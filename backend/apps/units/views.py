from rest_framework import filters, permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Unit
from .serializers import UnitSerializer


class UnitViewSet(BaseCondoViewSet):
    queryset = Unit.objects.prefetch_related("residents")
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "units.view",
        "retrieve": "units.view",
        "create": "units.create",
        "update": "units.update",
        "partial_update": "units.update",
        "destroy": "units.delete",
    }
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["number", "block", "code"]
    ordering_fields = ["number", "block", "created_at"]
