# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import pytest
import sys

windows = pytest.mark.skipif(sys.platform != 'win32', reason="requires windows")

win32only = pytest.mark.skipif("sys.platform != 'win32'")

skipIfDjangoVersion = lambda v: pytest.mark.skipif("django.VERSION[:2]>={}".format(v),
                                                   reason="Skip if django>={}".format(v))
