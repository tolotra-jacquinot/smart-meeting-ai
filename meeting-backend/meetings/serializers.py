import os
from rest_framework import serializers

from .models import Meeting, AudioFile


class MeetingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Meeting
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'source_language',
            'status',
            'meeting_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'owner',
            'status',
            'created_at',
            'updated_at',
        ]


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = [
            'id',
            'meeting',
            'file',
            'original_name',
            'duration',
            'uploaded_at',
        ]

        read_only_fields = [
            'id',
            'original_name',
            'duration',
            'uploaded_at',
        ]

    def validate_file(self, value):
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.webm']
        max_size = 1024 * 1024 * 1024  # 1 Go

        extension = os.path.splitext(value.name)[1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Format audio non autorisé. "
                "Formats acceptés : MP3, WAV, M4A, WEBM."
            )

        if value.size > max_size:
            raise serializers.ValidationError(
                "Le fichier audio ne doit pas dépasser 1 Go."
            )

        return value