from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import Announcement


class AnnouncementSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
