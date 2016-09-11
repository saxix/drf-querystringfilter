# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import pytest

from drf_querystringfilter.exceptions import InvalidPattern
from drf_querystringfilter.filters import RexList

logger = logging.getLogger(__name__)


def test_rexlist():
    l = RexList()
    l.append('.*')
    assert 1 in l
    assert '1' in l

    l = RexList()
    l.append(r'a?')
    l.append(r'b*')
    assert 'c' not in l
    assert 'b' in l
    assert 'aa' in l
    assert '^baa' not in l

    l = RexList()
    l.append(r'.*__')
    assert 'join__field' in l

    with pytest.raises(InvalidPattern):
        l.append('[*')

    l = RexList(['.*'])
    l[0] = '.*'
    with pytest.raises(InvalidPattern):
        l[0] = '[*'

    with pytest.raises(InvalidPattern):
        RexList(['.*', []])
