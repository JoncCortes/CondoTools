import csv
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import HasAnyRole
from apps.common.tenant import get_active_condominium_id
from apps.common.viewsets import BaseCondoViewSet

from .models import Package, PackageAuditLog
from .serializers import MarkPickedUpSerializer, PackageAuditLogSerializer, PackageSerializer


class PackagePermission(HasAnyRole):
    allowed_roles = ("SINDICO", "PORTEIRO", "MORADOR")


class PackageViewSet(BaseCondoViewSet):
    queryset = Package.objects.select_related("unit", "resident")
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated, PackagePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "delivery_type", "unit", "resident"]
    search_fields = ["description", "store", "bank", "tracking_code"]
    ordering_fields = ["received_at", "created_at", "status"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(status="DELIVERED")

    @action(detail=True, methods=["post"], url_path="mark-picked-up")
    def mark_picked_up(self, request, pk=None):
        package = self.get_object()
        serializer = MarkPickedUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        PackageAuditLog.objects.create(
            condominium=package.condominium,
            package=package,
            unit=package.unit,
            recipient_name=(package.resident.full_name if package.resident else ""),
            delivery_type=package.delivery_type,
            store=package.store,
            bank=package.bank,
            tracking_code=package.tracking_code,
            received_at=package.received_at,
            received_by=request.user,
            picked_up_at=timezone.now(),
            picked_up_by_user=request.user,
            picked_up_by_name=data["picked_up_by_name"],
            picked_up_by_document=data.get("picked_up_by_document", ""),
            picked_up_quantity=data.get("picked_up_quantity", 1),
            notes=data.get("notes", ""),
            action=data.get("action", "PICKED_UP"),
        )

        package.status = "DELIVERED" if data.get("action", "PICKED_UP") == "PICKED_UP" else "ARCHIVED"
        package.delivered_at = timezone.now()
        package.save(update_fields=["status", "delivered_at", "updated_at"])
        return Response({"detail": "Baixa registrada com sucesso."})


class PackageAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PackageAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, PackagePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["unit", "delivery_type", "store", "bank", "action", "picked_up_by_user", "created_at"]
    search_fields = ["recipient_name", "picked_up_by_name", "picked_up_by_document", "notes", "tracking_code"]
    ordering_fields = ["created_at", "picked_up_at"]

    def get_queryset(self):
        user = self.request.user
        qs = PackageAuditLog.objects.select_related("package", "unit", "picked_up_by_user")
        if user.is_superuser or user.role == user.Role.PLATFORM_ADMIN:
            condo_id = get_active_condominium_id(self.request)
            return qs.filter(condominium_id=condo_id) if condo_id else qs.none()
        return qs.filter(condominium_id=user.condominium_id)

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        qs = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="package_logs.csv"'
        writer = csv.writer(response)
        writer.writerow(["created_at", "unit", "recipient_name", "delivery_type", "store", "bank", "action", "picked_up_by_name"])
        for row in qs:
            writer.writerow([row.created_at, row.unit_id, row.recipient_name, row.delivery_type, row.store, row.bank, row.action, row.picked_up_by_name])
        return response
