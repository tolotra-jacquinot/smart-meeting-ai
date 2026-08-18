from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Meeting, AudioFile
from .serializers import MeetingSerializer, AudioFileSerializer

from .services.audio import (
    InvalidAudioError,
    validate_audio_with_ffprobe,
    get_audio_duration,
)


class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(
            owner=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(
            owner=self.request.user
        )


class AudioUploadView(generics.CreateAPIView):
    serializer_class = AudioFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        meeting = serializer.validated_data['meeting']

        if meeting.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to upload audio to this meeting."
            )

        uploaded_file = self.request.FILES.get('file')

        audio = serializer.save(
            original_name=uploaded_file.name if uploaded_file else ''
        )

        try:
            validate_audio_with_ffprobe(audio.file.path)
            duration = get_audio_duration(audio.file.path)

        except InvalidAudioError as exc:
            audio.file.delete(save=False)
            audio.delete()

            raise ValidationError({
                "file": str(exc)
            })

        audio.duration = duration
        audio.save(update_fields=['duration'])