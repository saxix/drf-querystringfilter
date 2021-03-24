try:
    from django.core.exceptions import FieldDoesNotExist
except ImportError:
    from django.db.models import FieldDoesNotExist
