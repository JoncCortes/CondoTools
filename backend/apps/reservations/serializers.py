from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source="unit.display_name", read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"
