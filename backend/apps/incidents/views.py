from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Incident
from .serializers import IncidentSerializer


class IncidentViewSet(BaseCondoViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "occurrences.view",
        "retrieve": "occurrences.view",
        "create": "occurrences.create",
        "update": "occurrences.update",
        "partial_update": "occurrences.update",
        "destroy": "occurrences.delete",
    }
    search_fields = ["title", "status"]
