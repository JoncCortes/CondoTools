from rest_framework import serializers

from .models import ServiceProvider, ServiceProviderAuditLog


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = "__all__"


class ServiceProviderAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderAuditLog
        fields = "__all__"
