from rest_framework import serializers

from .models import RolePermissionSet


class RolePermissionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermissionSet
        fields = "__all__"
