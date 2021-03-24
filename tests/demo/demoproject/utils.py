# -*- coding: utf-8 -*-
import sys
from datetime import datetime

import pytest
import six

windows = pytest.mark.skipif(sys.platform != 'win32', reason='requires windows')

win32only = pytest.mark.skipif("sys.platform != 'win32'")

skipIfDjangoVersion = lambda v: pytest.mark.skipif('django.VERSION[:2]>={}'.format(v),
                                                   reason='Skip if django>={}'.format(v))


class record(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        from demoproject.models import DemoModel
        from django.contrib.auth.models import User
        _id = self.kwargs.get('id', 1)
        self.u, __ = User.objects.get_or_create(username=str(_id), pk=_id)

        defaults = dict(fk=self.u,
                        id=_id,
                        logic=False,
                        char=str(_id),
                        date=datetime.today(),
                        choices=1,
                        # json={},
                        integer=_id)
        defaults.update(self.kwargs)
        self.obj = DemoModel.objects.create(**defaults)

    def __enter__(self):
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.obj.delete()
        self.u.delete()
        if exc_type:
            six.reraise(exc_type, exc_val, exc_tb)
