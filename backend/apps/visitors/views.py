from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Visitor
from .serializers import VisitorSerializer


class VisitorPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "PORTEIRO")


class VisitorViewSet(BaseCondoViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAuthenticated, VisitorPermission]
    search_fields = ["full_name", "document"]
