import pytest
from datetime import datetime


@pytest.fixture(scope='session')
def client(request):
    import django_webtest
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app

#
# @pytest.fixture(scope='session')
# def _django_db_setup(request,
#                      _django_test_environment,
#                      _django_cursor_wrapper,
#                      _django_db_setup):
#     with _django_cursor_wrapper:
#         from demoproject.models import DemoModel
#         # if request.config.option.create_db:
#         #     for i in range(100):
#         #         u = User.objects.create(username=str(i))
#         #
#         #         DemoModel.objects.create(fk=u,
#         #                                  logic=bool(i%2),
#         #                                  char=str(i),
#         #                                  date=datetime.today(),
#         #                                  choices=1,
#         #                                  integer=i)
