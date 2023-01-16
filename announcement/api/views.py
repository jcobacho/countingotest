from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from announcement.models import Announcement, Candidate
from entity.models import Developer


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

    @action(methods=["post"], detail=True)
    def accept(self, request, pk=None):
        self.object = self.get_object()
        Developer.objects.get_or_create(user_id=self.object.user.id)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def bulk_accept(self, request, pk=None):
        ids = request.data.get('ids')
        candidates = self.get_queryset().filter(id__in=ids).values_list('user_id', flat=True)

        for id in list(candidates):
            Developer.objects.get_or_create(user_id=id)

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def decline(self, request, pk=None):
        self.object = self.get_object()
        Developer.objects.filter(user_id=self.object.user.id).delete()

        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def bulk_decline(self, request, pk=None):
        ids = request.data.get('ids')
        candidates = self.get_queryset().filter(id__in=ids).values_list('user_id', flat=True)

        Developer.objects.filter(user_id__in=candidates).delete()

        return Response(status=status.HTTP_200_OK)
