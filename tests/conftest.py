import logging

import pytest

from demoproject.models import UserFactory, DemoModelFactory


@pytest.fixture()
def user(db):
    return UserFactory()


@pytest.fixture()
def demomodel(user):
    return DemoModelFactory(fk=user)


@pytest.fixture(scope='session')
def client(request):
    import django_webtest
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


def pytest_configure():
    logger = logging.getLogger("drf_querystringfilter")
    handler = logging.NullHandler()
    # handler = logging.StreamHandler()
    logger.handlers = [handler]
