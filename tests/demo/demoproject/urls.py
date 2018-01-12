from django.conf.urls import url

from demoproject.api import DemoModelView, Users

#
urlpatterns = (
    url(r'users', Users.as_view(), name='users'),
    url(r'demos', DemoModelView.as_view(), name='demos'),
)
