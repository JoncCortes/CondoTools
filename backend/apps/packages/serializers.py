from rest_framework import serializers

from .models import Package, PackageAuditLog


class PackageSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source="unit.display_name", read_only=True)

    class Meta:
        model = Package
        fields = "__all__"


class PackageAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageAuditLog
        fields = "__all__"


class MarkPickedUpSerializer(serializers.Serializer):
    picked_up_by_name = serializers.CharField()
    picked_up_by_document = serializers.CharField(required=False, allow_blank=True)
    picked_up_quantity = serializers.IntegerField(required=False, default=1)
    notes = serializers.CharField(required=False, allow_blank=True)
    action = serializers.ChoiceField(required=False, choices=["PICKED_UP", "RETURNED", "CANCELLED"], default="PICKED_UP")
