from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from announcement.models import Announcement, Candidate


class AnnouncementViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Announcement.objects.all()
    permission_classes = (AllowAny,)


class CandidateViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Candidate.objects.all()
    permission_classes = (AllowAny,)

    @action(methods=["delete"], detail=False)
    def bulk_delete(self, request, pk=None):

        ids = request.data.get('ids')
        self.get_queryset().filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
