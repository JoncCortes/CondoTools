from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsPlatformAdmin
from apps.common.tenant import get_active_condominium_id

from .models import CustomPage, MenuCategory, MenuItem
from .serializers import CustomPageSerializer, MenuCategorySerializer, MenuItemSerializer


class AdminOnlyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsPlatformAdmin]


class MenuCategoryViewSet(AdminOnlyModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemViewSet(AdminOnlyModelViewSet):
    queryset = MenuItem.objects.select_related("category", "condominium")
    serializer_class = MenuItemSerializer

    @action(detail=True, methods=["post"], url_path="move-up")
    def move_up(self, request, pk=None):
        item = self.get_object()
        item.order = max(item.order - 1, 0)
        item.save(update_fields=["order"])
        return Response(MenuItemSerializer(item).data)

    @action(detail=True, methods=["post"], url_path="move-down")
    def move_down(self, request, pk=None):
        item = self.get_object()
        item.order = item.order + 1
        item.save(update_fields=["order"])
        return Response(MenuItemSerializer(item).data)


class CustomPageViewSet(AdminOnlyModelViewSet):
    queryset = CustomPage.objects.select_related("category")
    serializer_class = CustomPageSerializer


class PublicMenuViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user: User = request.user
        role = user.role
        condo_id = get_active_condominium_id(request) if (user.is_superuser or role == User.Role.PLATFORM_ADMIN) else user.condominium_id

        global_items = MenuItem.objects.filter(enabled=True, condominium__isnull=True)
        condo_items = MenuItem.objects.filter(enabled=True, condominium_id=condo_id) if condo_id else MenuItem.objects.none()

        merged = {}
        for item in global_items:
            merged[item.key] = item
        for item in condo_items:
            merged[item.key] = item

        visible_items = [
            MenuItemSerializer(item).data
            for item in sorted(merged.values(), key=lambda i: (i.order, i.id))
            if not item.allowed_roles or role in item.allowed_roles or user.is_superuser
        ]

        custom_pages = CustomPage.objects.filter(enabled=True)
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
