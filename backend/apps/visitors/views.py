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

from .models import Visitor, VisitorAuditLog
from .serializers import VisitorAuditLogSerializer, VisitorSerializer


class VisitorViewSet(BaseCondoViewSet):
    queryset = Visitor.objects.select_related("unit")
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]

    permission_map = {
        "list": "visitors.view",
        "retrieve": "visitors.view",
        "create": "visitors.create",
        "update": "visitors.update",
        "partial_update": "visitors.update",
        "destroy": "visitors.delete",
        "mark_exit": "visit_logs.checkout",
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["unit", "is_active"]
    search_fields = ["full_name", "document"]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        visitor = serializer.instance
        VisitorAuditLog.objects.create(
            condominium=visitor.condominium,
            visitor=visitor,
            visitor_name=visitor.full_name,
            document=visitor.document,
            unit=visitor.unit,
            authorized_by=visitor.authorized_by,
            entry_at=timezone.now(),
            registered_by=self.request.user,
            notes=visitor.notes,
            status="INSIDE",
        )

    @action(detail=True, methods=["post"], url_path="mark-exit")
    def mark_exit(self, request, pk=None):
        visitor = self.get_object()
        latest = visitor.audit_logs.filter(status="INSIDE").order_by("-created_at").first()
        if latest:
            latest.exit_at = timezone.now()
            latest.finalized_by = request.user
            latest.status = "EXITED"
            latest.save(update_fields=["exit_at", "finalized_by", "status", "updated_at"])
        visitor.is_active = False
        visitor.save(update_fields=["is_active", "updated_at"])
        return Response({"detail": "Saída registrada com sucesso."})


class VisitorAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VisitorAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {"list": "visitors.audit_log.view", "retrieve": "visitors.audit_log.view", "export_csv": "visitors.audit_log.view"}
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["unit", "status", "registered_by", "finalized_by", "created_at"]
    search_fields = ["visitor_name", "document", "authorized_by", "notes"]
    ordering_fields = ["created_at", "entry_at", "exit_at"]

    def get_queryset(self):
        user = self.request.user
        qs = VisitorAuditLog.objects.select_related("unit", "registered_by", "finalized_by")
        if user.is_superuser or user.role == user.Role.PLATFORM_ADMIN:
            condo_id = get_active_condominium_id(self.request)
            return qs.filter(condominium_id=condo_id) if condo_id else qs.none()
        return qs.filter(condominium_id=user.condominium_id)

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        qs = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="visitor_logs.csv"'
        writer = csv.writer(response)
        writer.writerow(["created_at", "visitor_name", "document", "unit", "status", "entry_at", "exit_at", "registered_by"])
        for row in qs:
            writer.writerow([row.created_at, row.visitor_name, row.document, row.unit_id, row.status, row.entry_at, row.exit_at, row.registered_by_id])
        return response
