from rest_framework import serializers

from apps.accounts.models import RoleChoices

from .models import (
    Announcement,
    CommonArea,
    Condominium,
    Incident,
    Package,
    Reservation,
    Resident,
    Staff,
    Unit,
    VisitLog,
    Visitor,
)


class TenantSafeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        condo = attrs.get("condominium") or getattr(self.instance, "condominium", None)
        if user.is_platform_admin():
            return attrs
        if condo and condo.id != user.condominium_id:
            raise serializers.ValidationError("Condomínio inválido para o usuário autenticado.")
        return attrs


class CondominiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominium
        fields = "__all__"


class UnitSerializer(TenantSafeSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ResidentSerializer(TenantSafeSerializer):
    class Meta:
        model = Resident
        fields = "__all__"


class StaffSerializer(TenantSafeSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class VisitorSerializer(TenantSafeSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class VisitLogSerializer(TenantSafeSerializer):
    class Meta:
        model = VisitLog
        fields = "__all__"


class PackageSerializer(TenantSafeSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class AnnouncementSerializer(TenantSafeSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"


class IncidentSerializer(TenantSafeSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.setdefault("reporter", user)
        return super().create(validated_data)


class CommonAreaSerializer(TenantSafeSerializer):
    class Meta:
        model = CommonArea
        fields = "__all__"


class ReservationSerializer(TenantSafeSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        if user.role == RoleChoices.MORADOR:
            validated_data.setdefault("resident", user)
        return super().create(validated_data)
