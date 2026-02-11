from rest_framework import permissions

from apps.accounts.models import User
from apps.common.viewsets import BaseCondoViewSet

from .models import Condominium
from .serializers import CondominiumSerializer


class CondominiumViewSet(BaseCondoViewSet):
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "document"]

    def get_queryset(self):
        qs = super().get_queryset()
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return Condominium.objects.all()
        return Condominium.objects.filter(id=user.condominium_id)
