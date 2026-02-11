from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Resident
from .serializers import ResidentSerializer


class ResidentPermission(HasAnyRole):
    allowed_roles = ("SINDICO",)


class ResidentViewSet(BaseCondoViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, ResidentPermission]
    search_fields = ["full_name", "phone"]
