from rest_framework import permissions

from apps.accounts.models import RoleChoices
from apps.common.permissions import RolePermission
from apps.common.viewsets import CondoScopedModelViewSet

from .models import (
    Announcement,
    CommonArea,
    Condominium,
    Incident,
    Package,
    Reservation,
    Resident,
    Staff,
    Unit,
    VisitLog,
    Visitor,
)
from .serializers import (
    AnnouncementSerializer,
    CommonAreaSerializer,
    CondominiumSerializer,
    IncidentSerializer,
    PackageSerializer,
    ReservationSerializer,
    ResidentSerializer,
    StaffSerializer,
    UnitSerializer,
    VisitLogSerializer,
    VisitorSerializer,
)


class CondominiumViewSet(CondoScopedModelViewSet):
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "document"]
    ordering_fields = ["id", "name"]
    condo_field = "id"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_platform_admin():
            return qs
        return qs.filter(id=user.condominium_id)


class SindicoPermission(RolePermission):
    allowed_roles = (RoleChoices.SINDICO,)


class PortariaPermission(RolePermission):
    allowed_roles = (RoleChoices.SINDICO, RoleChoices.PORTEIRO)


class ResidentAccessPermission(RolePermission):
    allowed_roles = (RoleChoices.SINDICO, RoleChoices.MORADOR)


class UnitViewSet(CondoScopedModelViewSet):
    queryset = Unit.objects.select_related("condominium").all()
    serializer_class = UnitSerializer
    permission_classes = [SindicoPermission]
    search_fields = ["code", "block"]


class ResidentViewSet(CondoScopedModelViewSet):
    queryset = Resident.objects.select_related("condominium", "unit", "user").all()
    serializer_class = ResidentSerializer
    permission_classes = [SindicoPermission]
    search_fields = ["full_name", "phone"]


class StaffViewSet(CondoScopedModelViewSet):
    queryset = Staff.objects.select_related("condominium", "user").all()
    serializer_class = StaffSerializer
    permission_classes = [SindicoPermission]
    search_fields = ["full_name", "role_name"]


class VisitorViewSet(CondoScopedModelViewSet):
    queryset = Visitor.objects.select_related("condominium", "unit").all()
    serializer_class = VisitorSerializer
    permission_classes = [PortariaPermission]
    search_fields = ["full_name", "document"]


class VisitLogViewSet(CondoScopedModelViewSet):
    queryset = VisitLog.objects.select_related("condominium", "visitor").all()
    serializer_class = VisitLogSerializer
    permission_classes = [PortariaPermission]


class PackageViewSet(CondoScopedModelViewSet):
    queryset = Package.objects.select_related("condominium", "unit").all()
    serializer_class = PackageSerializer
    permission_classes = [PortariaPermission]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == RoleChoices.MORADOR:
            return qs.filter(unit__residents__user=user)
        return qs


class AnnouncementViewSet(CondoScopedModelViewSet):
    queryset = Announcement.objects.select_related("condominium").all()
    serializer_class = AnnouncementSerializer
    permission_classes = [ResidentAccessPermission]
    search_fields = ["title", "content"]


class IncidentViewSet(CondoScopedModelViewSet):
    queryset = Incident.objects.select_related("condominium", "reporter").all()
    serializer_class = IncidentSerializer
    permission_classes = [ResidentAccessPermission]


class CommonAreaViewSet(CondoScopedModelViewSet):
    queryset = CommonArea.objects.select_related("condominium").all()
    serializer_class = CommonAreaSerializer
    permission_classes = [ResidentAccessPermission]


class ReservationViewSet(CondoScopedModelViewSet):
    queryset = Reservation.objects.select_related("condominium", "common_area", "unit", "resident").all()
    serializer_class = ReservationSerializer
    permission_classes = [ResidentAccessPermission]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == RoleChoices.MORADOR:
            return qs.filter(resident=user)
        return qs
