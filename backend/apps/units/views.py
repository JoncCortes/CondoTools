from rest_framework import filters, permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Unit
from .serializers import UnitSerializer


class UnitPermission(HasAnyRole):
    allowed_roles = ("SINDICO",)


class UnitViewSet(BaseCondoViewSet):
    queryset = Unit.objects.prefetch_related("residents")
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated, UnitPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["number", "block", "code"]
    ordering_fields = ["number", "block", "created_at"]
