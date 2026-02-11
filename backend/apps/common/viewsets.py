from rest_framework import permissions, viewsets

from apps.accounts.models import User
from apps.common.permissions import IsSameCondominium
from apps.common.tenant import get_active_condominium_id, resolve_condominium_for_create


class BaseCondoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSameCondominium]

    def _is_condo_scoped(self, queryset) -> bool:
        model_fields = {f.name for f in queryset.model._meta.fields}
        return "condominium" in model_fields

    def get_queryset(self):
        queryset = super().get_queryset()
        user: User = self.request.user
        if not self._is_condo_scoped(queryset):
            return queryset

        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            condo_id = get_active_condominium_id(self.request)
            if condo_id:
                return queryset.filter(condominium_id=condo_id)
            return queryset.none()

        return queryset.filter(condominium_id=user.condominium_id)

    def perform_create(self, serializer):
        user: User = self.request.user
        fields = serializer.Meta.model._meta.fields
        if any(field.name == "condominium" for field in fields):
            payload_condo = serializer.validated_data.get("condominium")
            condo = resolve_condominium_for_create(
                request=self.request,
                user=user,
                payload_condominium=payload_condo,
            )
            serializer.save(condominium=condo)
            return
        serializer.save()
