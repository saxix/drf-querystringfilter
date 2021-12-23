class QueryFilterException(Exception):
    pass


class InvalidPattern(TypeError):
    def __init__(self, pattern, *args, **kwargs):
        msg = '{} is not a valid regular expression'.format(pattern)
        super().__init__(msg)


class InvalidQueryArgumentError(QueryFilterException):
    def __init__(self, field, *args, **kwargs):
        msg = "Invalid parameter '{}'".format(field)
        super().__init__(msg)


class InvalidQueryValueError(QueryFilterException):
    argument = ''

    def __init__(self, field, *args, **kwargs):
        msg = "Invalid value '{}' for parameter {}".format(field, self.argument)
        super().__init__(msg)


class InvalidFilterError(QueryFilterException):
    def __init__(self, field, *args, **kwargs):
        super().__init__("Invalid filter '{}'".format(field))


class FilteringError(QueryFilterException):
    def __init__(self, reason, *args, **kwargs):
        msg = "Invalid query: '{}'".format(reason)
        super().__init__(msg)
