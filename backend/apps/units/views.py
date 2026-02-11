from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Unit
from .serializers import UnitSerializer


class UnitPermission(HasAnyRole):
    allowed_roles = ("SINDICO",)


class UnitViewSet(BaseCondoViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated, UnitPermission]
    search_fields = ["code", "block"]
