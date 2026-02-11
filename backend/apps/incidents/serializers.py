from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import Incident


class IncidentSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"
