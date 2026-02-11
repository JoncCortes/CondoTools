from rest_framework import permissions

from apps.common.permissions import IsPlatformAdmin
from apps.common.viewsets import BaseCondoViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(BaseCondoViewSet):
    queryset = User.objects.select_related("condominium")
    serializer_class = UserSerializer
    search_fields = ["email", "first_name", "last_name"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsPlatformAdmin()]
        return [permissions.IsAuthenticated()]
