from rest_framework import serializers

from apps.accounts.models import User
from apps.units.models import Unit

from .models import Condominium


class CondominiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominium
        fields = "__all__"


class WizardSetupSerializer(serializers.Serializer):
    condominium_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    document = serializers.CharField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    syndic_first_name = serializers.CharField()
    syndic_last_name = serializers.CharField(required=False, allow_blank=True)
    syndic_email = serializers.EmailField()
    syndic_password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        if not attrs.get("condominium_id") and not attrs.get("name"):
            raise serializers.ValidationError({"name": ["Informe um condomínio existente ou crie um novo."]})
        return attrs


class UnitBulkCreateSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["range", "list"])
    block = serializers.CharField(required=False, allow_blank=True)
    start = serializers.IntegerField(required=False)
    end = serializers.IntegerField(required=False)
    list_text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs["mode"] == "range" and (attrs.get("start") is None or attrs.get("end") is None):
            raise serializers.ValidationError({"start": ["Informe início e fim do intervalo."]})
        if attrs["mode"] == "list" and not (attrs.get("list_text") or "").strip():
            raise serializers.ValidationError({"list_text": ["Cole uma lista de unidades."]})
        return attrs

    def build_units(self):
        attrs = self.validated_data
        if attrs["mode"] == "range":
            block = (attrs.get("block") or "").strip()
            return [{"number": str(i), "block": block} for i in range(attrs["start"], attrs["end"] + 1)]

        rows = []
        for raw in (attrs.get("list_text") or "").splitlines():
            line = raw.strip()
            if not line:
                continue
            if "-" in line:
                block, number = [x.strip() for x in line.split("-", 1)]
            else:
                block, number = (attrs.get("block") or "").strip(), line
            rows.append({"number": number, "block": block})
        return rows


def create_syndic(*, condominium: Condominium, first_name: str, last_name: str, email: str, password: str) -> User:
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "role": User.Role.SINDICO,
            "condominium": condominium,
        },
    )
    if not created:
        raise serializers.ValidationError({"syndic_email": ["Já existe usuário com este e-mail."]})
    user.set_password(password)
    user.save()
    return user


def create_units_in_bulk(*, condominium: Condominium, items: list[dict]) -> int:
    created = 0
    for item in items:
        block = item.get("block", "")
        number = item.get("number", "")
        code = f"{block}-{number}".strip("-")
        _, was_created = Unit.objects.get_or_create(
            condominium=condominium,
            number=number,
            block=block,
            defaults={"code": code},
        )
        if was_created:
            created += 1
    return created
