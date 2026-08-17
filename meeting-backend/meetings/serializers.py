from rest_framework import serializers
from .models import Meeting


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
