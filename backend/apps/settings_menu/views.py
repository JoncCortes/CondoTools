from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsPlatformAdmin

from .models import CustomPage, MenuCategory, MenuItem
from .serializers import CustomPageSerializer, MenuCategorySerializer, MenuItemSerializer


class AdminOnlyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]


class MenuCategoryViewSet(AdminOnlyModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemViewSet(AdminOnlyModelViewSet):
    queryset = MenuItem.objects.select_related("category")
    serializer_class = MenuItemSerializer


class CustomPageViewSet(AdminOnlyModelViewSet):
    queryset = CustomPage.objects.select_related("category")
    serializer_class = CustomPageSerializer


class PublicMenuViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user: User = request.user
        role = user.role
        items = MenuItem.objects.filter(enabled=True)
        custom_pages = CustomPage.objects.filter(enabled=True)

        visible_items = [
            MenuItemSerializer(item).data
            for item in items
            if not item.allowed_roles or role in item.allowed_roles or user.is_superuser
        ]
        visible_pages = [
            CustomPageSerializer(page).data
            for page in custom_pages
            if not page.allowed_roles or role in page.allowed_roles or user.is_superuser
        ]
        return Response({"menu_items": visible_items, "custom_pages": visible_pages})


class PublicCustomPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomPageSerializer
    lookup_field = "slug"

    def get_queryset(self):
        user: User = self.request.user
        role = user.role
        pages = CustomPage.objects.filter(enabled=True)
        if user.is_superuser:
            return pages
        ids = [p.id for p in pages if not p.allowed_roles or role in p.allowed_roles]
        return pages.filter(id__in=ids)
