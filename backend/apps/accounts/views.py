from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsPlatformAdmin
from apps.common.viewsets import BaseCondoViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(BaseCondoViewSet):
    queryset = User.objects.select_related("condominium")
    serializer_class = UserSerializer
    search_fields = ["email", "first_name", "last_name"]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "list"}:
            return [permissions.IsAuthenticated(), IsPlatformAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(UserSerializer(request.user).data)
