from __future__ import absolute_import, unicode_literals

import json
import operator

import django
import pytest
from rest_framework.test import APIRequestFactory

from demoproject.api import DemoModelView
from demoproject.models import DemoModel
from demoproject.utils import record

try:
    from django.urls import reverse # django 2.0
except ImportError:
    from django.core.urlresolvers import reverse


factory = APIRequestFactory()
uri = reverse('demos')


def assert_result(res, field, value):
    j = json.loads(res.content.decode('utf-8'))
    values = list(map(operator.itemgetter(field), j))
    if callable(value):
        return all(value(i) for i in values)
    else:
        return all(i == value for i in values)


class TestEqual(object):
    def setup(self):
        self.view = DemoModelView.as_view()
        self.uri = reverse('demos')

    @pytest.mark.django_db
    def test_equal_integer(self):
        with record():
            request = factory.get(self.uri, {'integer': 1})
            response = self.view(request).render()
            j = json.loads(response.content.decode('utf-8'))
            assert j[0]['integer'] == 1

    @pytest.mark.django_db
    def test_equal_logic(self):
        with record(logic=True) as rec:
            request = factory.get(self.uri, {'logic': 'true'})
            response = self.view(request).render()
            j = json.loads(response.content.decode('utf-8'))
            assert j[0]['logic'] == rec.logic

    @pytest.mark.django_db
    def test_equal_date(self):
        with record(json={}, date='2000-01-01', ) as rec:
            request = factory.get(self.uri, {'date': '2000-01-01'})
            response = self.view(request).render()
            j = json.loads(response.content.decode('utf-8'))
            assert j[0]['date'] == rec.date


class TestOperator(object):
    def setup(self):
        self.view = DemoModelView.as_view()
        self.uri = reverse('demos')

    @pytest.mark.django_db
    def test_equal(self):
        request = factory.get(self.uri, {'char': 1})
        response = self.view(request).render()
        assert assert_result(response, 'char', '1')

    @pytest.mark.django_db
    def test_logic(self):
        request = factory.get(self.uri, {'logic': False})
        response = self.view(request).render()
        assert assert_result(response, 'logic', False)

    @pytest.mark.django_db
    def test_is(self):
        request = factory.get(self.uri, {'logic__is': False})
        response = self.view(request).render()
        assert assert_result(response, 'logic', False)

    @pytest.mark.django_db
    def test_inlist(self):
        request = factory.get(self.uri, {'integer__inlist': '1,2,3'})
        response = self.view(request).render()
        assert assert_result(response, 'fk', lambda i: i in [1, 2, 3])

    @pytest.mark.django_db
    def test_in(self):
        request = factory.get(self.uri, {'integer__in': [1,3]})
        response = self.view(request).render()
        assert assert_result(response, 'fk', lambda i: i in [1, 3])

    @pytest.mark.django_db
    def test_isnull(self):
        request = factory.get(self.uri, {'fk__isnull': 1})
        response = self.view(request).render()
        assert assert_result(response, 'fk', lambda i: i is None)
        # j = json.loads(response.content)
        # values = map(operator.itemgetter('fk'), j)
        # assert all(i is None for i in values)

    @pytest.mark.django_db
    def test_not_inlist(self):
        request = factory.get(self.uri, {'integer__not_inlist': '1,2,3'})
        response = self.view(request).render()
        assert assert_result(response, 'integer', lambda i: i not in [1, 2, 3])

    @pytest.mark.django_db
    def test_not_in(self):
        request = factory.get(self.uri, {'integer__not_in': [1,3]})
        response = self.view(request).render()
        assert assert_result(response, 'integer', lambda i: i not in [1, 3])

        # j = json.loads(response.content)
        # values = map(operator.itemgetter('fk'), j)
        # assert all(i is None for i in values)

    @pytest.mark.django_db
    def test_not(self):
        request = factory.get(self.uri, {'logic__not': True})
        response = self.view(request).render()
        assert assert_result(response, 'logic', lambda i: not i)

    @pytest.mark.django_db
    def test_greater_than(self):
        request = factory.get(self.uri, {'fk__gt': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = list(map(operator.itemgetter('fk'), j))
        assert all(i > 1 for i in values)

    @pytest.mark.django_db
    def test_less_than(self):
        request = factory.get(self.uri, {'fk__lt': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = list(map(operator.itemgetter('fk'), j))
        assert all(i < 1 for i in values)

    @pytest.mark.django_db
    def test_contains(self):
        request = factory.get(self.uri, {'char__contains': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = list(map(operator.itemgetter('char'), j))
        assert all('1' in i for i in values)

    @pytest.mark.django_db
    def test_startswith(self):
        request = factory.get(self.uri, {'char__startswith': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = list(map(operator.itemgetter('char'), j))
        assert all(i.startswith('1') for i in values)

    @pytest.mark.django_db
    def test_endswith(self):
        request = factory.get(self.uri, {'char__endswith': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = list(map(operator.itemgetter('char'), j))
        assert all(i.endswith('1') for i in values)


class TestAttributes(object):
    def setup(self):
        self.view = DemoModelView.as_view()
        self.uri = reverse('demos')

    @pytest.mark.django_db
    def test_filter_fields(self, monkeypatch):
        request = factory.get(uri, {'xxxx': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 400
        assert j == {u"detail": u"Invalid filter 'xxxx'"}, j


@pytest.mark.skipif(django.VERSION < (1, 9), reason="django<1.9")
class TestJsonField(object):
    def setup(self):
        self.view = DemoModelView.as_view()
        self.uri = reverse('demos')
        self.rec1 = record(id=1,
            # username=str(time.time()),
            json={'a': {'b': {'c': [11, 22, 33],
                              'd': 'xyz',
                              'e': 2222,
                              'f': ['aa/11', 'bb/22', 'cc/33']}
                        }
                  }).obj

        self.rec2 = record(
            id=2,
            # fk=None,
            # username=str(time.time()),
            json={'a': {'b': {'c': [1, 2, 3],
                              'd': 'abc',
                              'e': 22,
                              'f': ['a/1', 'b/2', 'c/3']}
                        }
                  }).obj

    def teardown(self):
        self.rec1.delete()
        self.rec2.delete()

    @pytest.mark.django_db
    def test_filter_contains_str1(self, client):
        if django.VERSION >= (1, 10):
            target = 'a/1'
        else:
            target = '"a/1"'

        res = client.get('{}?json__a__b__f__contains={}'.format(self.uri, target))
        j = json.loads(res.content.decode('utf-8'))
        value = list(map(operator.itemgetter('json'), j))[0]
        assert res.status_code == 200
        assert value['a']['b']['c'] == [1, 2, 3]

    @pytest.mark.django_db
    def test_filter_inarray(self, client):

        res = client.get('{}?json__a__b__f__inarray=a/1'.format(self.uri))
        j = json.loads(res.content.decode('utf-8'))
        value = list(map(operator.itemgetter('json'), j))[0]
        assert res.status_code == 200
        assert value['a']['b']['c'] == [1, 2, 3]

    @pytest.mark.django_db
    def test_filter_int_inarray(self, client):
        rec1 = DemoModel.objects.get(json__a__b__d='abc')
        rec2 = DemoModel.objects.get(json__a__b__e=22)
        rec3 = DemoModel.objects.get(json__a__b__c__contains=[3])
        target = 3
        assert rec1.pk == rec2.pk == rec3.pk == self.rec2.pk

        res = client.get('{}?json__a__b__c__int_inarray={}'.format(self.uri, target))
        j = json.loads(res.content.decode('utf-8'))
        value = list(map(operator.itemgetter('json'), j))[0]
        assert res.status_code == 200
        assert value['a']['b']['c'] == [1, 2, 3]
