# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
# from factory import DjangoModelFactory, SubFactory, Sequence
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory


class DemoModel(models.Model):
    fk = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           blank=True, null=True)
    char = models.CharField('Chäř', max_length=255, blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)
    logic = models.BooleanField(default=False, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    decimal = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    float = models.FloatField(blank=True, null=True)
    bigint = models.BigIntegerField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    json = JSONField(blank=True, null=True)
    nullable = models.CharField(max_length=255, null=True, default=None)
    choices = models.IntegerField(choices=((1, 'Choice 1'), (2, 'Choice 2'), (3, 'Choice 3')),
                                  blank=True, null=True)

    class Meta:
        app_label = 'demoproject'


class UserFactory(DjangoModelFactory):
    id = Sequence(lambda x: 10+x)
    username = Sequence(lambda x: "User%s" % x)

    class Meta:
        model = User


class DemoModelFactory(DjangoModelFactory):
    fk = SubFactory(UserFactory)

    class Meta:
        model = DemoModel
