from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import Visitor, VisitorAuditLog


class VisitorSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    unit_display = serializers.CharField(source="unit.display_name", read_only=True)

    class Meta:
        model = Visitor
        fields = "__all__"


class VisitorAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorAuditLog
        fields = "__all__"
