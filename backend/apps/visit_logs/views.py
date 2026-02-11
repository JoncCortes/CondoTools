from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import VisitLog
from .serializers import VisitLogSerializer


class VisitLogViewSet(BaseCondoViewSet):
    queryset = VisitLog.objects.select_related("visitor")
    serializer_class = VisitLogSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "visit_logs.view",
        "retrieve": "visit_logs.view",
        "create": "visit_logs.create",
        "update": "visit_logs.update",
        "partial_update": "visit_logs.update",
        "destroy": "visit_logs.delete",
    }
    search_fields = ["visitor__full_name", "notes"]
