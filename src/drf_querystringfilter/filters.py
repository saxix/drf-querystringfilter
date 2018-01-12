# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import re

from .exceptions import InvalidPattern


def parse_bool(value):
    if str(value).lower() in ['true', '1']:
        return True
    elif str(value).lower() in ['false', '0']:
        return False
    else:
        return bool(value)


class RexList(list):
    """
        list class where each entry is a valid regular expression

    >>> r = RexList(["a.*"])
    >>> r.append("[0-9]*")
    >>> "1" in r
    True

    >>> "cc" in r
    False

    >>> "abc" in r
    True

    >>> print(r)
    [u'a.*', u'[0-9]*']

    >>> r[0] = '.*'

    >>> r[0] = '[0-'
    Traceback (most recent call last):
        ...
    InvalidPattern: [0- is not a valid regular expression
    """

    def __init__(self, seq=None):
        regexx = []
        if seq:
            for el in seq:
                regexx.append(self._compile(el))
        super(RexList, self).__init__(regexx)

    def __repr__(self):
        return str([r.pattern for r in self])

    def _compile(self, pattern, index=None):
        try:
            return re.compile(pattern)
        except (TypeError, re.error):
            raise InvalidPattern(pattern)

    def __setitem__(self, i, pattern):
        rex = self._compile(pattern)
        super(RexList, self).__setitem__(i, rex)

    def append(self, pattern):
        rex = self._compile(pattern)
        super(RexList, self).append(rex)

    def __contains__(self, target):
        t = str(target)
        for rex in self:
            m = rex.match(t)
            if m and m.group():
                return True
        return False
