from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "MORADOR")


class AnnouncementViewSet(BaseCondoViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, AnnouncementPermission]
    search_fields = ["title", "content"]
