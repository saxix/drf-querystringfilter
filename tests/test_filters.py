from datetime import datetime
from inspect import isclass

import pytest
from demoproject.api import DemoModelViewSet
from demoproject.models import UserFactory
from demoproject.utils import record
from rest_framework.test import APIClient

from drf_querystringfilter.backend import QueryStringFilterBackend
from drf_querystringfilter.exceptions import InvalidQueryArgumentError


@pytest.fixture
def data():
    return [
        record(id=1, char='a', integer=1000, logic=True, date=datetime(2000, 1, 1), fk=UserFactory(id=11, username='User1')),
        record(id=2, char='b', integer=2000, logic=False, date=datetime(2000, 2, 1), fk=UserFactory(id=12, username='User2')),
        record(id=3, char='c', integer=3000, logic=None, date=datetime(2000, 3, 1), fk=UserFactory(id=13, username='User3')),
        record(id=4, char=None, integer=None, logic=None, date=None, fk=None),
        record(id=5, char='', integer=0, logic=None, date=datetime(2000, 5, 1), fk=UserFactory(id=15, username='User5'))
    ]


CHARS = [('char=a', 1),
         ('char__in=a,c', 2),
         ('char__contains=a', 1),
         ('char__icontains=a', 1),
         ('char__istartswith=a', 1),
         ('char__endswith=a', 1),
         ('char__gt=x', 0),
         ('char__lt=b', 2),
         ('char__gte=b', 2),
         ('char=', 1),
         ('char__isnull=1', 1),
         ('char__isnull=0', 4),
         ('char!=a', 4),
         ('char__in!=a,b,c', 2),
         ]
BOOLEAN = [('logic=true', 1),
           ('logic__isnull=true', 3),
           ('logic!=true', 4),
           ('logic__isnull!=true', 2),
           ('logic=22', Exception),
           ]

DATES = [('date=2000-1-1', 1),
         ('date__gt=2000-1-1', 3),
         ('date__lt=2000-2-1', 1),
         ('date__year=2000', 4),
         ('date__month=2', 1),
         ('date__month__gt=1', 3),
         ('date__month__gt=1&date__month__lt=3', 1),
         ]

INTEGER = [
    ('integer=1000', 1),
    ('integer!=1000', 4),
    ('integer__gt=1000', 2),
    ('integer__lt=2000', 2),
    ('integer__gt=1000&integer__lt=3000', 1),
]

FK = [
    ('fk=11', 1),
    ('fk__username=User1', 1),
    ('fk__username__contains=1', 1),
    ('fk__username__icontains=user1', 1),
    ('fk__username__icontains=user', 4),
    ('fk__isnull=true', 1),
    ('fk__isnull!=true', 4),
    ('fk__isnull=false', 4),
]

# for processors tests
# logic=True is added in processor logic
#
PROCESSOR = [
    ('processor=1000', 1),
    ('processor__gt=1000', 2),
    ('processor__lt=2000', 2),
    ('processor!=1000', 4),
]


@pytest.fixture
def backend():
    return QueryStringFilterBackend()


@pytest.fixture
def view():
    return DemoModelViewSet.as_view({'get': 'list'})


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.parametrize('flt,expected', CHARS, ids=[i[0] for i in CHARS])
def test_char(db, flt, expected, api_client, view, data):
    res = api_client.get('/demos/?%s' % flt)
    assert len(res.json()) == expected, res.json()


@pytest.mark.parametrize('flt,expected', BOOLEAN, ids=[i[0] for i in BOOLEAN])
def test_bool(db, flt, expected, api_client, data):
    if isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(expected):
            api_client.get('/demos/?%s' % flt)
    else:
        res = api_client.get('/demos/?%s' % flt)
        assert len(res.json()) == expected, res.json()


@pytest.mark.parametrize('flt,expected', DATES, ids=[i[0] for i in DATES])
def test_dates(db, flt, expected, api_client, view, data):
    res = api_client.get('/demos/?%s' % flt)
    assert len(res.json()) == expected, [res.json()]


@pytest.mark.parametrize('flt,expected', INTEGER, ids=[i[0] for i in INTEGER])
def test_integer(db, flt, expected, api_client, view, data):
    res = api_client.get('/demos/?%s' % flt)
    assert len(res.json()) == expected, res.json()


@pytest.mark.parametrize('flt,expected', FK, ids=[i[0] for i in FK])
def test_fk(db, flt, expected, api_client, data):
    res = api_client.get('/demos/?%s' % flt)
    assert len(res.json()) == expected, res.json()


@pytest.mark.parametrize('flt,expected', PROCESSOR, ids=[i[0] for i in PROCESSOR])
def test_processor(db, flt, expected, api_client, data):
    if isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(InvalidQueryArgumentError):
            api_client.get('/demos/?%s' % flt)
    else:
        res = api_client.get('/demos/?%s' % flt)
        assert len(res.json()) == expected, res.json()


def test_excluded(db, api_client, data):
    res = api_client.get('/demos/?excluded1=1')
    assert len(res.json()) == 5


def test_ignored(db, api_client, data):
    res = api_client.get('/demos/?ignored1=1')
    assert len(res.json()) == 5


@pytest.mark.parametrize('flt', ['forbidden1=1', 'forbidden3=1'])
def test_filter_blacklist(db, api_client, flt, data):
    with pytest.raises(InvalidQueryArgumentError):
        api_client.get('/demos/?%s' % flt)
