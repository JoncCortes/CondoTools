from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import VisitLog


class VisitLogSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = VisitLog
        fields = "__all__"
