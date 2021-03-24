from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from demoproject.models import DemoModel

from drf_querystringfilter.backend import QueryStringFilterBackend


class CustomQueryStringFilterBackend(QueryStringFilterBackend):
    excluded_query_params = ['excluded1']

    def process_processor(self, filters, exclude, value, op, **payload):
        if payload['param'].endswith("!"):
            return {}, {'integer__%s' % op: value}
        return {'integer__%s' % op: value}, {}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    filter_fields = ['username', 'email', 'is_staff', 'date_joined', 'processor']
    filter_blacklist = None
    filter_backends = (CustomQueryStringFilterBackend,)
    queryset = User.objects.all()


class DemoModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='fk.username', read_only=True)
    fk = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    alias = serializers.CharField(source='char')

    class Meta:
        model = DemoModel
        exclude = ()


class DemoModelViewSet(ModelViewSet):
    serializer_class = DemoModelSerializer
    filter_fields = ['fk', 'char', 'integer', 'logic', 'date', 'json', 'processor']
    filter_backends = (CustomQueryStringFilterBackend,)
    filter_blacklist = ['forbidden[0-9]',]
    queryset = DemoModel.objects.all()

    def drf_ignore_filter(self, request, field):
        return field == 'ignored1'
