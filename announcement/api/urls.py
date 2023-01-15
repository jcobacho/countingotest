from rest_framework.routers import DefaultRouter
from announcement.api.views import AnnouncementViewSet

router = DefaultRouter()
router.register("announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = [] + router.urls
