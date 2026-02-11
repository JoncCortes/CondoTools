from rest_framework import permissions

from apps.common.permissions import HasRBACPermission
from apps.common.viewsets import BaseCondoViewSet

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(BaseCondoViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, HasRBACPermission]
    permission_map = {
        "list": "reservations.view",
        "retrieve": "reservations.view",
        "create": "reservations.create",
        "update": "reservations.update",
        "partial_update": "reservations.update",
        "destroy": "reservations.delete",
    }
    search_fields = ["status"]
