# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from collections import OrderedDict
from functools import lru_cache

from django import forms
from django.conf import settings
from django.db.models import BooleanField, CharField, FieldDoesNotExist
from django.template import loader
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from .exceptions import FilteringError, InvalidFilterError, InvalidQueryArgumentError, QueryFilterException, \
    InvalidQueryValueError
from .filters import RexList, parse_bool

logger = logging.getLogger(__name__)


class QueryStringFilterBackend(BaseFilterBackend):
    template = "querystringfilter/filter.html"
    form_prefix = ''
    allowed_joins = -1
    field_casting = {}

    def get_form_class(self, request, view):
        fields = OrderedDict([
            (name, forms.CharField(required=False))
            for name in view.filter_fields])

        return type(str('%sForm' % self.__class__.__name__),
                    (forms.Form,), fields)

    def get_form(self, request, view):
        if not hasattr(self, '_form'):
            Form = self.get_form_class(request, view)
            self._form = Form(request.GET, prefix=self.form_prefix)
        return self._form

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = {'form': self.get_form(request, view)}
        return template.render(context, request)

    @property
    def query_params(self):
        """
        More semantically correct name for request.GET.
        """
        return self.request._request.GET

    @property
    def excluded_query_params(self):
        params_list = [api_settings.URL_FORMAT_OVERRIDE]
        return params_list

    def ignore_filter(self, request, field, view):
        if hasattr(view, 'drf_ignore_filter'):
            return view.drf_ignore_filter(request, field)
        return False

    def _get_mapping(self, view):
        if hasattr(view, 'get_serializer'):
            # try:
            return view.get_serializer().fields
        else:
            # except AttributeError:
            return {}

    def _get_filters(self, request, queryset, view):  # noqa
        """
        filter queryset based on http querystring arguments

        Accepted synthax:

        - exclude null values: country__not=><
        - only values in list: &country__id__in=176,20
        - exclude values in list: &country__id__not_in=176,20

        """

        def field_type(field_name):
            try:
                field_object = opts.get_field(field_name)
                if isinstance(field_object, BooleanField):
                    return bool
            except FieldDoesNotExist:
                return self.field_casting.get(field_name, str)

        filter_fields = getattr(view, 'filter_fields', None)
        exclude = {}
        filters = {}

        if filter_fields:
            blacklist = RexList(getattr(view, 'filter_blacklist', []))
            mapping = self._get_mapping(view)

            opts = queryset.model._meta
            for fieldname_arg in self.query_params:
                raw_value = self.query_params.get(fieldname_arg)

                if fieldname_arg[-1] == "!":
                    filter_field_name = fieldname_arg[:-1]
                    TARGET = exclude
                else:
                    TARGET = filters
                    filter_field_name = fieldname_arg

                if filter_field_name in self.excluded_query_params:
                    continue
                if self.ignore_filter(request, filter_field_name, view):
                    continue
                try:
                    if filter_field_name in blacklist:
                        raise InvalidQueryArgumentError(fieldname_arg)
                    parts = None
                    if '__' in filter_field_name:
                        parts = filter_field_name.split('__')
                        filter_field_name = parts[0]
                        op = parts[-1]
                    else:
                        op = 'exact'

                    #     parts = [field_name]

                    processor = getattr(self, 'process_{}'.format(filter_field_name), None)
                    # if (field_name not in filter_fields) and (not processor):
                    #     raise InvalidQueryArgumentError(fieldname_arg)
                    # field is configured in Serializer
                    # so we use 'source' attribute
                    if filter_field_name in mapping:
                        real_field_name = mapping[filter_field_name].source
                        # if '.' in real_field_name:
                        #     real_field_name = real_field_name.split('.')[0]
                        # field_name = real_field_name.replace('.', '__')
                    else:
                        real_field_name = filter_field_name

                    if processor:
                        payload = {'field': filter_field_name,
                                   'request': request,
                                   'param': fieldname_arg,
                                   'op': op,
                                   'field_name': real_field_name,
                                   'parts': parts,
                                   'value': raw_value,
                                   'real_field_name': real_field_name}
                        _f, _e = processor(dict(filters), dict(exclude), **payload)
                        filters.update(**_f)
                        exclude.update(**_e)
                    else:
                        # field_object = opts.get_field(real_field_name)
                        value_type = field_type(real_field_name)
                        if parts:
                            f = "{}__{}".format(real_field_name, "__".join(parts[1:]))
                        else:
                            f = filter_field_name
                        if op == 'in':
                            value = raw_value.split(',')
                        elif op == 'isnull':
                            value = parse_bool(raw_value)
                        elif value_type == bool:
                            value = parse_bool(raw_value)
                        else:
                            value = raw_value
                        TARGET[f] = value

                except ValueError as e:
                    raise InvalidQueryValueError(e)
                except QueryFilterException as e:
                    raise
                except Exception as e:
                    raise InvalidFilterError(fieldname_arg)
        return filters, exclude

    def filter_queryset(self, request, queryset, view):
        self.request = request
        try:
            self.filters, self.exclude = self._get_filters(request, queryset, view)
            qs = queryset.filter(**self.filters).exclude(**self.exclude)
            logger.debug("""Filtering using:
{}
{}""".format(self.filters, self.exclude))
            # if '_distinct' in self.query_params:
            #     f = self.get_param_value('_distinct')
            #     qs = qs.order_by(*f).distinct(*f)
            return qs
        except (InvalidFilterError, QueryFilterException) as e:
            logger.exception(e)
            raise
        # except Exception as e:
        #     logger.exception(e)
        #     raise FilteringError(e)
