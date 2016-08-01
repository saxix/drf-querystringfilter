# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import pytest
from django.utils.translation import gettext as _
from django_dynamic_fixture import G
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from demoproject.api import DemoModelView
from demoproject.models import DemoModel
from drf_querystringfilter.backend import QueryStringFilterBackend
from drf_querystringfilter.exceptions import InvalidFilterError, FilteringError

logger = logging.getLogger(__name__)


def assert_queryset_values(qs, field, value):
    return all(getattr(rec, field) == value for rec in qs.all())


@pytest.fixture
def backend():
    return QueryStringFilterBackend()


@pytest.fixture
def view(rf):
    request = Request(rf.get(b''))
    return DemoModelView(request=request,
                         queryset=DemoModel.objects.all(),
                         format_kwarg=None)


@pytest.mark.django_db
def test_invalid_filter(backend, view, rf):
    request = Request(rf.get(b'/aaa/?a=1'))

    with pytest.raises(InvalidFilterError):
        backend.filter_queryset(request, view.queryset, view)


@pytest.mark.django_db
def test_processor(backend, view, rf, monkeypatch):
    def process_custom(*k, **kw):
        filters = {'id': 1}
        return filters, {}

    monkeypatch.setattr(backend, 'process_custom', process_custom, False)
    request = Request(rf.get(b'/aaa/?custom=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('id')) == [{u'id': 1}]


@pytest.mark.django_db
def test_processor_alter_filter(backend, view, rf, monkeypatch):
    def process_fk(*k, **kw):
        return {'fk__id': 2}, {}

    monkeypatch.setattr(view, 'filter_fields', ['fk'])
    monkeypatch.setattr(backend, 'process_fk', process_fk, False)
    request = Request(rf.get('/aaa/?fk__id=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('id')) == [{'id': 2}]


@pytest.mark.django_db
def test_processor_operator(backend, view, rf, monkeypatch):
    def process_ignore(*k, **kw):
        return {'fk__exact': 2}, {}

    monkeypatch.setattr(view, 'filter_fields', ['fk'])
    monkeypatch.setattr(backend, 'process_ignore', process_ignore, False)
    request = Request(rf.get('/aaa/?fk__ignore=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('id')) == [{'id': 2}]


@pytest.mark.django_db
def test_equal(backend, view, rf, monkeypatch):
    request = Request(rf.get('/aaa/?id=1'))
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('id')) == [{'id': 1}]


@pytest.mark.django_db
def test_equal(backend, view, rf, monkeypatch):
    request = Request(rf.get(b'/aaa/?char=1'))
    monkeypatch.setattr(view, 'filter_fields', ['char'])

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('char')) == [{'char': '1'}]


@pytest.mark.django_db
def test_not(backend, view, rf, monkeypatch):
    request = Request(rf.get('/aaa/?id__not=1'))
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    qs = backend.filter_queryset(request, view.queryset, view)
    assert not qs.filter(id=1)


@pytest.mark.django_db
def test_lte(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['id'])
    request = Request(rf.get('/aaa/?id__lte=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('id')) == [{'id': 1}]


@pytest.mark.django_db
def test_is(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['logic'])
    G(DemoModel, logic=True, fk=None)
    request = Request(rf.get('/aaa/?logic__is=true'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values('logic')) == [{u'logic': True}]


@pytest.mark.django_db
def test_in(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    request = Request(rf.get('/aaa/?id__in=1,2,3'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert list(qs.values_list('id', flat=True)) == [1, 2, 3]


@pytest.mark.django_db
def test_not_in(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    request = Request(rf.get(b'/aaa/?id__not_in=1,2,3'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert not qs.filter(id__in=[1, 2, 3])


@pytest.mark.django_db
def test_null(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['null_logic'])

    request = Request(rf.get('/aaa/?null_logic__isnull=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert assert_queryset_values(qs, 'null_logic', None)


@pytest.mark.django_db
def test_empty_value_ignored(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    request = Request(rf.get(b'/aaa/?id='))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert assert_queryset_values(qs, 'null_logic', None)


@pytest.mark.django_db
def test_join(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['fk'])

    request = Request(rf.get(b'/aaa/?fk__id=2'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert qs.filter(fk__id=2).exists()


@pytest.mark.django_db
def test_join_invalid(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['fk'])

    request = Request(rf.get(b'/aaa/?fk__invalid=2'))

    with pytest.raises(FilteringError):
        backend.filter_queryset(request, view.queryset, view)




@pytest.mark.django_db
def test_blacklist(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['fk'])
    monkeypatch.setattr(view, 'filter_blacklist', ['.*__'])

    request = Request(rf.get(b'/aaa/?fk__id=2'))

    with pytest.raises(InvalidFilterError):
        backend.filter_queryset(request, view.queryset, view)


@pytest.mark.django_db
def test_source(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['alias'])

    request = Request(rf.get(b'/aaa/?alias=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert qs.filter(fk__username=1).exists()


@pytest.mark.django_db
def test_source_join(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['username'])

    request = Request(rf.get(b'/aaa/?username=1'))

    qs = backend.filter_queryset(request, view.queryset, view)
    assert qs.filter(fk__username=1).exists()



@pytest.mark.django_db
def test_invalid_filter(backend, view, rf, monkeypatch):
    monkeypatch.setattr(view, 'filter_fields', ['id'])

    request = Request(rf.get(b'/aaa/?id=a'))

    with pytest.raises(FilteringError):
        backend.filter_queryset(request, view.queryset, view)
