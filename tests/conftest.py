import pytest
from django_dynamic_fixture import G


@pytest.fixture(scope='session')
def client(request):
    import django_webtest
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


@pytest.fixture(scope='session')
def _django_db_setup(request,
                     _django_test_environment,
                     _django_cursor_wrapper,
                     _django_db_setup):
    with _django_cursor_wrapper:
        from demoproject.models import DemoModel
        if request.config.option.create_db:
            G(DemoModel, n=100)
