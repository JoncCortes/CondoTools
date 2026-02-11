from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import Resident


class ResidentSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    unit_display = serializers.CharField(source="unit.display_name", read_only=True)

    class Meta:
        model = Resident
        fields = "__all__"
