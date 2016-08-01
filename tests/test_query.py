from __future__ import absolute_import, unicode_literals
import operator
import pytest
from django_dynamic_fixture import G
from rest_framework.serializers import json, reverse
from rest_framework.test import APIRequestFactory

from demoproject.api import Users, DemoModelView
from demoproject.models import DemoModel

factory = APIRequestFactory()
uri = reverse('demos')


def assert_result(res, field, value):
    j = json.loads(res.content.decode('utf-8'))
    values = map(operator.itemgetter(field), j)
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
        request = factory.get(self.uri, {'integer': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        assert j[0]['integer'] == 1

    @pytest.mark.django_db
    def test_equal_logic(self):
        rec = G(DemoModel, logic=True, fk=None)
        request = factory.get(self.uri, {'logic': 'true'})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        assert j[0]['logic'] == rec.logic

    @pytest.mark.django_db
    def test_equal_date(self):
        rec = G(DemoModel, date='2000-01-01', fk=None)
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
    def test_is(self):
        request = factory.get(self.uri, {'logic': False})
        response = self.view(request).render()
        assert assert_result(response, 'logic', False)

    @pytest.mark.django_db
    def test_is(self):
        request = factory.get(self.uri, {'logic__is': False})
        response = self.view(request).render()
        assert assert_result(response, 'logic', False)

    @pytest.mark.django_db
    def test_in(self):
        request = factory.get(self.uri, {'integer__in': "1,2,3"})
        response = self.view(request).render()
        assert assert_result(response, 'fk', lambda i: i in [1, 2, 3])

    @pytest.mark.django_db
    def test_isnull(self):
        request = factory.get(self.uri, {'fk__isnull': 1})
        response = self.view(request).render()
        assert assert_result(response, 'fk', lambda i: i is None)
        # j = json.loads(response.content)
        # values = map(operator.itemgetter("fk"), j)
        # assert all(i is None for i in values)

    @pytest.mark.django_db
    def test_not_in(self):
        request = factory.get(self.uri, {'integer__not_in': "1,2,3"})
        response = self.view(request).render()
        assert assert_result(response, 'integer', lambda i: i not in [1, 2, 3])

        # j = json.loads(response.content)
        # values = map(operator.itemgetter("fk"), j)
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
        values = map(operator.itemgetter("fk"), j)
        assert all(i > 1 for i in values)

    @pytest.mark.django_db
    def test_less_than(self):
        request = factory.get(self.uri, {'fk__lt': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = map(operator.itemgetter("fk"), j)
        assert all(i < 1 for i in values)

    @pytest.mark.django_db
    def test_contains(self):
        request = factory.get(self.uri, {'char__contains': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = map(operator.itemgetter("char"), j)
        assert all('1' in i for i in values)

    @pytest.mark.django_db
    def test_startswith(self):
        request = factory.get(self.uri, {'char__startswith': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = map(operator.itemgetter("char"), j)
        assert all(i.startswith('1') for i in values)

    @pytest.mark.django_db
    def test_endswith(self):
        request = factory.get(self.uri, {'char__endswith': 1})
        response = self.view(request).render()
        j = json.loads(response.content.decode('utf-8'))
        values = map(operator.itemgetter("char"), j)
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
        assert j == {u'detail': u"Invalid filter 'xxxx'"}
