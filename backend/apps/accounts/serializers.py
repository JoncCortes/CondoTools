from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "condominium", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def validate(self, attrs):
        role = attrs.get("role", getattr(self.instance, "role", None))
        condominium = attrs.get("condominium", getattr(self.instance, "condominium", None))

        if role == User.Role.PLATFORM_ADMIN:
            attrs["condominium"] = None
        elif role in {User.Role.SINDICO, User.Role.PORTEIRO, User.Role.MORADOR} and condominium is None:
            raise serializers.ValidationError({"condominium": ["Condomínio é obrigatório para o perfil selecionado."]})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError({"password": ["Senha é obrigatória."]})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
