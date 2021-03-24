from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from demoproject.api import DemoModelViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'demos', DemoModelViewSet)
urlpatterns = router.urls
#
# urlpatterns = (
#     url(r'users', Users.as_view(), name='users'),
#     url(r'demos', DemoModelView.as_view(), name='demos'),
# )
