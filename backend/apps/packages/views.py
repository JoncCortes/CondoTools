from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Package
from .serializers import PackageSerializer


class PackagePermission(HasAnyRole):
    allowed_roles = ("SINDICO", "PORTEIRO", "MORADOR")


class PackageViewSet(BaseCondoViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated, PackagePermission]
    search_fields = ["description"]
