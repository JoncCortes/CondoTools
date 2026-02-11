from rest_framework import serializers

from .models import Visitor, VisitorAuditLog


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class VisitorAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorAuditLog
        fields = "__all__"
