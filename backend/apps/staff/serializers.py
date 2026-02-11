from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import Staff


class StaffSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
