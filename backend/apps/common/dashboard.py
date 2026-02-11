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
                    "units_total": 0,
                    "residents_total": 0,
                    "visitors_today": 0,
                    "packages_pending": 0,
                    "incidents_open": 0,
                    "reservations_upcoming": 0,
                    "common_areas_total": 0,
                    "message": "Selecione um condomínio ativo.",
                }
            )

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        in_7_days = timezone.now() + timedelta(days=7)

        data = {
            "units_total": Unit.objects.filter(condominium_id=condo_id).count(),
            "residents_total": Resident.objects.filter(condominium_id=condo_id).count(),
            "visitors_today": VisitLog.objects.filter(condominium_id=condo_id, entry_at__gte=today_start).count(),
            "packages_pending": Package.objects.filter(condominium_id=condo_id, delivered_at__isnull=True).count(),
            "incidents_open": Incident.objects.filter(condominium_id=condo_id, status__iexact="OPEN").count(),
            "reservations_upcoming": Reservation.objects.filter(
                condominium_id=condo_id,
                start_at__gte=timezone.now(),
                start_at__lte=in_7_days,
            ).count(),
            "common_areas_total": CommonArea.objects.filter(condominium_id=condo_id).count(),
        }
        return Response(data)
