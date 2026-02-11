from rest_framework import serializers

from apps.accounts.models import User
from apps.common.tenant import get_active_condominium_id
from apps.condominiums.models import Condominium


class CondoScopedSerializerMixin(serializers.ModelSerializer):
    """Makes condominium non-required in payload and resolves it from context/user/header."""

    def get_fields(self):
        fields = super().get_fields()
        condo_field = fields.get("condominium")
        if condo_field:
            condo_field.required = False
            condo_field.allow_null = True
            condo_field.read_only = True
        return fields

    def _resolve_condominium(self):
        request = self.context.get("request")
        if not request or not getattr(request, "user", None) or not request.user.is_authenticated:
            raise serializers.ValidationError({"detail": "Usuário autenticado é obrigatório."})

        user: User = request.user
        payload_condo = self.initial_data.get("condominium") if hasattr(self, "initial_data") else None

        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            if payload_condo:
                condo = Condominium.objects.filter(pk=payload_condo).first()
                if not condo:
                    raise serializers.ValidationError({"condominium": ["Condomínio inválido."]})
                return condo

            condo_id = get_active_condominium_id(request)
            if condo_id:
                condo = Condominium.objects.filter(pk=condo_id).first()
                if condo:
                    return condo
                raise serializers.ValidationError({"condominium": ["Condomínio ativo inválido."]})

            raise serializers.ValidationError({"condominium": ["Selecione um condomínio ativo."]})

        if not user.condominium_id:
            raise serializers.ValidationError({"condominium": ["Seu usuário não está vinculado a um condomínio."]})
        return user.condominium

    def create(self, validated_data):
        if "condominium" not in validated_data or validated_data.get("condominium") is None:
            validated_data["condominium"] = self._resolve_condominium()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("condominium", None)
        return super().update(instance, validated_data)
