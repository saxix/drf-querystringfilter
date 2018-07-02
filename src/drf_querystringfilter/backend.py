# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

# from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
from django.db.models import BooleanField, CharField
from rest_framework.filters import BaseFilterBackend

from .exceptions import FilteringError, InvalidFilterError, InvalidQueryArgumentError
from .filters import RexList, parse_bool

logger = logging.getLogger(__name__)


class QueryStringFilterBackend(BaseFilterBackend):
    @property
    def query_params(self):
        """
        More semantically correct name for request.GET.
        """
        return self.request._request.GET

    @property
    def excluded_query_params(self):
        params_list = ['_distinct']
        format_param = "format"
        if hasattr(settings, "URL_FORMAT_OVERRIDE"):
            format_param = settings.URL_FORMAT_OVERRIDE
        params_list.append(format_param)
        return params_list

    def ignore_filter(self, request, field, view):
        if hasattr(view, 'drf_ignore_filter'):
            return view.drf_ignore_filter(request, field)
        return False

    def filter_queryset(self, request, queryset, view):  # noqa
        self.request = request
        try:
            f, e = self._get_filters(request, queryset, view)
            qs = queryset.filter(**f).exclude(**e)
            logger.debug("""Filtering using:
{}
{}""".format(f, e))
            if '_distinct' in self.query_params:
                f = self.query_params.getlist('_distinct')
                qs = qs.order_by(*f).distinct(*f)
            return qs
        except (InvalidFilterError, InvalidQueryArgumentError) as e:
            logger.exception(e)
            raise
        except Exception as e:
            logger.exception(e)
            raise FilteringError(e)

    def _get_filters(self, request, queryset, view):  # noqa
        """
        filter queryset based on http querystring arguments

        Accepted synthax:

        - exclude null values: country__not=><
        - only values in list: &country__id__in=176,20
        - exclude values in list: &country__id__not_in=176,20

        """
        filter_fields = getattr(view, 'filter_fields', None)
        exclude = {}
        filters = {}

        if filter_fields:
            blacklist = RexList(getattr(view, 'filter_blacklist', []))
            if hasattr(view, 'get_serializer'):
                mapping = view.get_serializer().fields
            else:
                mapping = {}
            opts = queryset.model._meta
            for fieldname_arg in self.query_params:
                if fieldname_arg in self.excluded_query_params:
                    continue
                try:
                    value = self.query_params.getlist(fieldname_arg)
                    value = list(filter(lambda x: x, value))
                    if not value:
                        continue

                    if self.ignore_filter(request, fieldname_arg, view):
                        continue

                    if fieldname_arg in blacklist:
                        raise InvalidQueryArgumentError(fieldname_arg)
                    parts = None
                    if '__' in fieldname_arg:
                        parts = fieldname_arg.split('__')
                        field_name = parts[0]
                    else:
                        field_name = fieldname_arg

                    processor = getattr(self, 'process_{}'.format(field_name), None)

                    if (field_name not in filter_fields) and (not processor):
                        raise InvalidQueryArgumentError(fieldname_arg)
                    # field is configured in Serializer
                    # so we use 'source' attribute
                    if field_name in mapping:
                        origin = mapping[field_name].source
                        if '.' in origin:
                            origin = origin.split('.')[0]
                        field_name = origin.replace('.', '__')
                    else:
                        origin = field_name

                    # check if exixts
                    # self.process_<FIELD_NAME> or
                    # self.process_<OP>
                    if processor:
                        payload = {'field': fieldname_arg,
                                   'request': request,
                                   'field_name': field_name,
                                   'parts': parts,
                                   'value': value,
                                   'origin': origin}
                        filters, exclude = processor(filters, exclude, **payload)
                    elif parts:
                        op = parts[-1]
                        processor = getattr(self, 'process_{}'.format(op), None)
                        if processor:
                            payload = {'field': fieldname_arg,
                                       'request': request,
                                       'field_name': field_name,
                                       'parts': parts,
                                       'value': value,
                                       'origin': origin}
                            filters, exclude = processor(filters, exclude, **payload)

                        else:
                            value = value[0]
                            if op == 'is':
                                value = parse_bool(value)
                                f = "{}".format(origin)
                                filters[f] = value
                            elif op == 'in':
                                value = value.split(',')
                                f = "__".join([origin] + parts[1:])
                                filters[f] = value
                            elif op == 'isnull':
                                value = parse_bool(value)
                                f = "__".join([origin] + parts[1:])
                                filters[f] = value
                            elif op == 'not_in':
                                value = value.split(',')
                                exclude["{}__in".format(origin)] = value
                            elif op == 'not':
                                f = "__".join([origin] + parts[1:-1])
                                exclude[f] = value

                            # elif op == 'contains_int':
                            #     f = "__".join([origin] + parts[1:-1]) + "__contains"
                            #     filters[f] = [int(value)]
                            # elif op == 'acontains':
                            #     f = "__".join([origin] + parts[1:-1]) + "__contains"
                            #     filters[f] = [value]
                            elif op == 'int_inarray':
                                f = "__".join([origin] + parts[1:-1]) + "__contains"
                                filters[f] = [int(value)]
                            elif op == 'inarray':
                                f = "__".join([origin] + parts[1:-1]) + "__contains"
                                filters[f] = [value]
                            else:
                                f = "{}__{}".format(origin, "__".join(parts[1:]))
                                filters[f] = value
                    else:
                        # try:
                        field_object = opts.get_field(origin)
                        if isinstance(field_object, CharField):
                            field_name = "{}__iexact".format(origin)
                            filters[field_name] = value[0]
                        elif isinstance(field_object, BooleanField):
                            filters[field_name] = parse_bool(value)
                        else:
                            filters[field_name] = value[0]

                        # except FieldDoesNotExist:
                        #     filters[origin] = value
                except Exception as e:
                    # raise
                    logger.exception(e)
                    raise InvalidFilterError(fieldname_arg)
        return filters, exclude
