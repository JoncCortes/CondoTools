from rest_framework import permissions, viewsets

from apps.accounts.models import User
from apps.common.permissions import IsSameCondominium


class BaseCondoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSameCondominium]

    def get_queryset(self):
        queryset = super().get_queryset()
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return queryset
        model_fields = {f.name for f in queryset.model._meta.fields}
        if "condominium" in model_fields:
            return queryset.filter(condominium_id=user.condominium_id)
        return queryset.none()

    def perform_create(self, serializer):
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            serializer.save()
            return
        fields = serializer.Meta.model._meta.fields
        if any(field.name == "condominium" for field in fields):
            serializer.save(condominium=user.condominium)
            return
        serializer.save()
