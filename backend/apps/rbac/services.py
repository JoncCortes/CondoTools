from apps.accounts.models import User
from apps.common.tenant import get_active_condominium_id

from .models import RolePermissionSet
from .registry import ROLE_DEFAULTS


def get_permissions_for_user(user: User, request=None):
    if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
        return ROLE_DEFAULTS[User.Role.PLATFORM_ADMIN]

    condo_id = user.condominium_id
    if request and (user.is_superuser or user.role == User.Role.PLATFORM_ADMIN):
        condo_id = get_active_condominium_id(request)

    scoped = RolePermissionSet.objects.filter(role=user.role, condominium_id=condo_id).first() if condo_id else None
    if scoped:
        return scoped.permissions or []

    global_set = RolePermissionSet.objects.filter(role=user.role, condominium__isnull=True).first()
    if global_set:
        return global_set.permissions or []

    return ROLE_DEFAULTS.get(user.role, [])


def user_has_permission(user: User, key: str, request=None) -> bool:
    if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
        return True
    return key in get_permissions_for_user(user, request=request)
