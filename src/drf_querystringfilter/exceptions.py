# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework.exceptions import ParseError

QueryFilterException = Exception


class InvalidPattern(TypeError):
    def __init__(self, pattern, *args, **kwargs):
        msg = '{} is not a valid regular expression'.format(pattern)
        super(InvalidPattern, self).__init__(msg)


class InvalidQueryArgumentError(QueryFilterException):
    def __init__(self, field, *args, **kwargs):
        msg = "Invalid parameter '{}'".format(field)
        super(InvalidQueryArgumentError, self).__init__(msg)


# class InvalidQueryValueError(QueryFilterException):
#     argument = ''
#
#     def __init__(self, field, *args, **kwargs):
#         msg = "Invalid value '{}' for parameter {}".format(field, self.argument)
#         super(InvalidQueryValueError, self).__init__(msg)
#

class InvalidFilterError(ParseError):
    def __init__(self, field, *args, **kwargs):
        super(InvalidFilterError, self).__init__("Invalid filter '{}'".format(field))


class FilteringError(QueryFilterException):
    def __init__(self, reason, *args, **kwargs):
        msg = "Invalid query: '{}'".format(reason)
        super(FilteringError, self).__init__(msg)
