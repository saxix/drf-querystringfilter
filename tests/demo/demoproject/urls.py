from demoproject.api import DemoModelViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'demos', DemoModelViewSet)
urlpatterns = router.urls
