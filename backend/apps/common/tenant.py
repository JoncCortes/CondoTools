from typing import Optional

from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.condominiums.models import Condominium

HEADER_NAME = "HTTP_X_CONDOMINIUM_ID"


def get_active_condominium_id(request) -> Optional[int]:
    raw = request.META.get(HEADER_NAME)
    if not raw:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise ValidationError({"condominium": ["Header X-CONDOMINIUM-ID inválido."]})


def resolve_condominium_for_create(*, request, user: User, payload_condominium):
    if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
        if payload_condominium:
            return payload_condominium
        condo_id = get_active_condominium_id(request)
        if condo_id:
            condo = Condominium.objects.filter(pk=condo_id).first()
            if condo:
                return condo
            raise ValidationError({"condominium": ["Condomínio ativo inválido."]})
        raise ValidationError({"condominium": ["Selecione um condomínio ativo."]})
    return user.condominium
