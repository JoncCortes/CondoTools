from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(BaseCondoViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "announcements.view",
        "retrieve": "announcements.view",
        "create": "announcements.create",
        "update": "announcements.update",
        "partial_update": "announcements.update",
        "destroy": "announcements.delete",
    }
    search_fields = ["title", "content"]
