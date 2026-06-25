from rest_framework.routers import DefaultRouter

from .views import StatusViewSet, UserViewSet

router = DefaultRouter()
router.register("statuses", StatusViewSet, basename="status")
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls
