from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsPlatformAdmin
from apps.common.viewsets import BaseCondoViewSet

from .serializers import UserSerializer


class UserViewSet(BaseCondoViewSet):
    queryset = User.objects.select_related("condominium")
    serializer_class = UserSerializer
    search_fields = ["email", "first_name", "last_name"]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "list", "set_password"}:
            return [permissions.IsAuthenticated(), IsPlatformAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return self.queryset
        return self.queryset.filter(condominium_id=user.condominium_id)

    def perform_create(self, serializer):
        # Users are managed by platform admins and may or may not belong to a condominium,
        # so we must not force condominium injection from BaseCondoViewSet.
        serializer.save()

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=True, methods=["post"], url_path="set-password")
    def set_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get("password")
        if not new_password:
            return Response({"password": ["Informe a nova senha."]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response({"detail": "Senha atualizada com sucesso."})
