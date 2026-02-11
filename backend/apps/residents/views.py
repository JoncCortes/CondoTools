from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Resident
from .serializers import ResidentSerializer


class ResidentViewSet(BaseCondoViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "residents.view",
        "retrieve": "residents.view",
        "create": "residents.create",
        "update": "residents.update",
        "partial_update": "residents.update",
        "destroy": "residents.delete",
    }
    search_fields = ["full_name", "phone"]
