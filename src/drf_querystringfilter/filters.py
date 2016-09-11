# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import re

from .exceptions import InvalidPattern

logger = logging.getLogger(__name__)


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
    """

    def __init__(self, seq=None):
        regexx = []
        if seq:
            for el in seq:
                try:
                    regexx.append(re.compile(el))
                except (TypeError, re.error):
                    raise InvalidPattern(el)
        super(RexList, self).__init__(regexx)

    def __repr__(self):
        return str([r.pattern for r in self])

    def __setitem__(self, i, y):
        try:
            rex = re.compile(y)
        except (TypeError, re.error):
            raise InvalidPattern(y)
        super(RexList, self).__setitem__(i, rex)

    def append(self, pattern):
        try:
            rex = re.compile(pattern)
        except (TypeError, re.error):
            raise InvalidPattern(pattern)
        super(RexList, self).append(rex)

    def __contains__(self, target):
        for rex in self:
            m = rex.match(str(target))
            if m and m.group():
                return True
        return False
