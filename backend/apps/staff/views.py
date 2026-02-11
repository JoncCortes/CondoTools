from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Staff
from .serializers import StaffSerializer


class StaffPermission(HasAnyRole):
    allowed_roles = ("SINDICO",)


class StaffViewSet(BaseCondoViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, StaffPermission]
    search_fields = ["full_name", "role_name"]
