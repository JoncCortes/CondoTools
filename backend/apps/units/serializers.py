from rest_framework import serializers

from .models import Unit


class UnitSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)
    resident_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Unit
        fields = [
            "id",
            "condominium",
            "number",
            "block",
            "floor",
            "notes",
            "code",
            "display_name",
            "resident_count",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "code": {"required": False, "allow_blank": True},
        }

    def validate_number(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Informe o número da unidade.")
        return value

    def _build_code(self, attrs):
        number = attrs.get("number", "")
        block = attrs.get("block", "")
        return f"{block}-{number}".strip("-")

    def create(self, validated_data):
        validated_data["code"] = self._build_code(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        merged = {
            "number": validated_data.get("number", instance.number),
            "block": validated_data.get("block", instance.block),
        }
        validated_data["code"] = self._build_code(merged)
        return super().update(instance, validated_data)

    def get_resident_count(self, obj):
        return obj.residents.count()
