from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsPlatformAdmin

from .models import RolePermissionSet
from .registry import PERMISSION_LABELS, PERMISSION_REGISTRY, ROLE_DEFAULTS
from .serializers import RolePermissionSetSerializer
from .services import get_permissions_for_user


class PermissionRegistryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"groups": PERMISSION_REGISTRY, "labels": PERMISSION_LABELS})


class MyPermissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        perms = get_permissions_for_user(request.user, request=request)
        return Response({
            "role": request.user.role,
            "condominium": request.user.condominium_id,
            "permissions": perms,
        })


class RolePermissionSetViewSet(viewsets.ModelViewSet):
    serializer_class = RolePermissionSetSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]
    queryset = RolePermissionSet.objects.select_related("condominium", "updated_by")

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get("role")
        if role:
            qs = qs.filter(role=role)
        return qs

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="restore-defaults")
    def restore_defaults(self, request, pk=None):
        instance = self.get_object()
        instance.permissions = ROLE_DEFAULTS.get(instance.role, [])
        instance.updated_by = request.user
        instance.save(update_fields=["permissions", "updated_by", "updated_at"])
        return Response(self.get_serializer(instance).data)
