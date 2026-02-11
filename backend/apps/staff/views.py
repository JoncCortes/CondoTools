from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Staff
from .serializers import StaffSerializer


class StaffViewSet(BaseCondoViewSet):
    queryset = Staff.objects.select_related("user")
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "residents.view",
        "retrieve": "residents.view",
        "create": "residents.create",
        "update": "residents.update",
        "partial_update": "residents.update",
        "destroy": "residents.delete",
    }
    search_fields = ["full_name", "role_name"]
