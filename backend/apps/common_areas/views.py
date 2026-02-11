from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import CommonArea
from .serializers import CommonAreaSerializer


class CommonAreaViewSet(BaseCondoViewSet):
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "common_areas.view",
        "retrieve": "common_areas.view",
        "create": "common_areas.create",
        "update": "common_areas.update",
        "partial_update": "common_areas.update",
        "destroy": "common_areas.delete",
    }
    search_fields = ["name"]
