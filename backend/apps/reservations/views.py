from rest_framework import permissions

from apps.common.permissions import HasAnyRole
from apps.common.viewsets import BaseCondoViewSet

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationPermission(HasAnyRole):
    allowed_roles = ("SINDICO", "MORADOR")


class ReservationViewSet(BaseCondoViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, ReservationPermission]
    search_fields = ["status"]
