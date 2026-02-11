from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Incident
from .serializers import IncidentSerializer


class IncidentPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "MORADOR")


class IncidentViewSet(BaseCondoViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated, IncidentPermission]
    search_fields = ["title", "status"]
