from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer, CharField

from demoproject.models import DemoModel
from drf_querystringfilter.backend import QueryStringFilterBackend


class UserSerializer(ModelSerializer):
    class Meta:
        model = User


class Users(ListAPIView):
    serializer_class = UserSerializer
    filter_fields = ['username', 'email', 'is_staff', 'date_joined']
    filter_blacklist = None
    filter_backends = (QueryStringFilterBackend,)
    queryset = User.objects.all()


class DemoModelSerializer(ModelSerializer):
    username = CharField(source='fk.username')
    alias = CharField(source='char')

    class Meta:
        model = DemoModel


class DemoModelView(ListAPIView):
    serializer_class = DemoModelSerializer
    filter_fields = ['fk', 'char', 'integer', 'logic', 'date']
    filter_blacklist = None
    filter_backends = (QueryStringFilterBackend,)
    queryset = DemoModel.objects.all()
