from rest_framework import serializers

from .models import Resident


class ResidentSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source="unit.display_name", read_only=True)

    class Meta:
        model = Resident
        fields = "__all__"
