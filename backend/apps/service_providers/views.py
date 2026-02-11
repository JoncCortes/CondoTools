import csv
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import HasRBACPermission
from apps.common.tenant import get_active_condominium_id
from apps.common.viewsets import BaseCondoViewSet

from .models import ServiceProvider, ServiceProviderAuditLog
from .serializers import ServiceProviderAuditLogSerializer, ServiceProviderSerializer


class ServiceProviderViewSet(BaseCondoViewSet):
    queryset = ServiceProvider.objects.select_related("unit")
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]

    permission_map = {
        "list": "service_providers.view",
        "retrieve": "service_providers.view",
        "create": "service_providers.create",
        "update": "service_providers.update",
        "partial_update": "service_providers.update",
        "destroy": "service_providers.delete",
        "mark_exit": "service_providers.update",
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["unit", "status", "service_type"]
    search_fields = ["provider_name", "company", "document", "service_type"]

    def get_queryset(self):
        return super().get_queryset().exclude(status="FINISHED")

    def perform_create(self, serializer):
        super().perform_create(serializer)
        provider = serializer.instance
        ServiceProviderAuditLog.objects.create(
            condominium=provider.condominium,
            service_provider=provider,
            provider_name=provider.provider_name,
            company=provider.company,
            document=provider.document,
            service_type=provider.service_type,
            unit=provider.unit,
            entry_at=timezone.now(),
            authorized_by=provider.authorized_by,
            registered_by=self.request.user,
            notes=provider.notes,
            status="ACTIVE",
        )

    @action(detail=True, methods=["post"], url_path="mark-exit")
    def mark_exit(self, request, pk=None):
        provider = self.get_object()
        latest = provider.audit_logs.filter(status="ACTIVE").order_by("-created_at").first()
        if latest:
            latest.exit_at = timezone.now()
            latest.finalized_by = request.user
            latest.status = "FINISHED"
            latest.save(update_fields=["exit_at", "finalized_by", "status", "updated_at"])
        provider.status = "FINISHED"
        provider.save(update_fields=["status", "updated_at"])
        return Response({"detail": "Saída do prestador registrada."})


class ServiceProviderAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceProviderAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {"list": "service_providers.audit_log.view", "retrieve": "service_providers.audit_log.view", "export_csv": "service_providers.audit_log.view"}
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["unit", "status", "service_type", "registered_by", "finalized_by", "created_at"]
    search_fields = ["provider_name", "company", "document", "notes", "authorized_by"]
    ordering_fields = ["created_at", "entry_at", "exit_at"]

    def get_queryset(self):
        user = self.request.user
        qs = ServiceProviderAuditLog.objects.select_related("unit", "registered_by", "finalized_by")
        if user.is_superuser or user.role == user.Role.PLATFORM_ADMIN:
            condo_id = get_active_condominium_id(self.request)
            return qs.filter(condominium_id=condo_id) if condo_id else qs.none()
        return qs.filter(condominium_id=user.condominium_id)

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        qs = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="service_provider_logs.csv"'
        writer = csv.writer(response)
        writer.writerow(["created_at", "provider_name", "company", "document", "service_type", "status", "entry_at", "exit_at"])
        for row in qs:
            writer.writerow([row.created_at, row.provider_name, row.company, row.document, row.service_type, row.status, row.entry_at, row.exit_at])
        return response
