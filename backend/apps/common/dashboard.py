from datetime import timedelta

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.common.tenant import get_active_condominium_id
from apps.common_areas.models import CommonArea
from apps.incidents.models import Incident
from apps.packages.models import Package
from apps.reservations.models import Reservation
from apps.residents.models import Resident
from apps.service_providers.models import ServiceProviderAuditLog
from apps.units.models import Unit
from apps.visit_logs.models import VisitLog


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get_condominium_id(self, user: User):
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return get_active_condominium_id(self.request)
        return user.condominium_id

    def get(self, request):
        user: User = request.user
        condo_id = self.get_condominium_id(user)
        if not condo_id:
            return Response(
                {
                    "total_units": 0,
                    "total_residents": 0,
                    "visitors_today": 0,
                    "service_providers_today": 0,
                    "packages_pending": 0,
                    "incidents_open": 0,
                    "reservations_upcoming": 0,
                    "message": "Selecione um condomínio ativo.",
                }
            )

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        in_7_days = timezone.now() + timedelta(days=7)

        data = {
            "total_units": Unit.objects.filter(condominium_id=condo_id).count(),
            "total_residents": Resident.objects.filter(condominium_id=condo_id).count(),
            "visitors_today": VisitLog.objects.filter(condominium_id=condo_id, entry_at__gte=today_start).count(),
            "service_providers_today": ServiceProviderAuditLog.objects.filter(
                condominium_id=condo_id,
                created_at__gte=today_start,
            ).count(),
            "packages_pending": Package.objects.filter(condominium_id=condo_id, status="PENDING").count(),
            "incidents_open": Incident.objects.filter(condominium_id=condo_id, status__iexact="OPEN").count(),
            "reservations_upcoming": Reservation.objects.filter(
                condominium_id=condo_id,
                start_at__gte=timezone.now(),
                start_at__lte=in_7_days,
            ).count(),
        }
        data["common_areas_total"] = CommonArea.objects.filter(condominium_id=condo_id).count()
        data["units_total"] = data["total_units"]
        data["residents_total"] = data["total_residents"]
        return Response(data)
