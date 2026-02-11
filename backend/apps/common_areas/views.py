from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import CommonArea
from .serializers import CommonAreaSerializer


class CommonAreaPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "MORADOR")


class CommonAreaViewSet(BaseCondoViewSet):
    queryset = CommonArea.objects.all()
    serializer_class = CommonAreaSerializer
    permission_classes = [permissions.IsAuthenticated, CommonAreaPermission]
    search_fields = ["name"]
