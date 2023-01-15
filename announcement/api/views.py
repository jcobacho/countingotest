from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from announcement.models import Announcement, Candidate


class AnnouncementViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny,)


class CandidateViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Candidate.objects.all()
    permission_classes = (AllowAny,)
