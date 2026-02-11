from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import VisitLog
from .serializers import VisitLogSerializer


class VisitLogPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "PORTEIRO")


class VisitLogViewSet(BaseCondoViewSet):
    queryset = VisitLog.objects.select_related("visitor")
    serializer_class = VisitLogSerializer
    permission_classes = [permissions.IsAuthenticated, VisitLogPermission]
    search_fields = ["visitor__full_name", "notes"]
