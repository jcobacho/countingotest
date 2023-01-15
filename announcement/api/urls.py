from rest_framework.routers import DefaultRouter
from announcement.api.views import AnnouncementViewSet, CandidateViewSet

router = DefaultRouter()
router.register("announcements", AnnouncementViewSet, basename="announcement")
router.register("candidates", CandidateViewSet, basename="candidate")

urlpatterns = [] + router.urls
