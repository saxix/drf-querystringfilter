from django.conf.urls import url

from demoproject.api import Users, DemoModelView

urlpatterns = (
    url(r'users', Users.as_view(), name='users'),
    url(r'demos', DemoModelView.as_view(), name='demos'),
)
