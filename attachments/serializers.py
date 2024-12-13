from django.conf import settings
from rest_framework import serializers

from attachments.models import AudioAttachment, FileAttachment
from attachments.utils.formatter import Formatter


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['src'] = f"{settings.CURRENT_URL}{instance.src}"
        data['size'] = Formatter.format_bytes(bytes_num=instance.size)

        return data


class AudioAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAttachment
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['src'] = f"{settings.CURRENT_URL}{instance.src}"

        return data
