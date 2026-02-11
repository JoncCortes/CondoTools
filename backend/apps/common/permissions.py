from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class _RolePermission(BasePermission):
    role: str | None = None

    def has_permission(self, request, view):
        user: User = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.role == self.role))


class IsPlatformAdmin(_RolePermission):
    role = User.Role.PLATFORM_ADMIN


class IsSyndic(_RolePermission):
    role = User.Role.SINDICO


class IsDoorman(_RolePermission):
    role = User.Role.PORTEIRO


class IsResident(_RolePermission):
    role = User.Role.MORADOR


class IsSameCondominium(BasePermission):
    def has_object_permission(self, request, view, obj):
        user: User = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return True
        obj_condo_id = getattr(obj, "condominium_id", None)
        return bool(obj_condo_id and user.condominium_id == obj_condo_id)


class HasAnyRole(BasePermission):
    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        user: User = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return True
        return user.role in self.allowed_roles
