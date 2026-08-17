from django.urls import path

from .views import (
    MeetingListCreateView,
    MeetingDetailView,
)


urlpatterns = [
    path(
        'meetings/',
        MeetingListCreateView.as_view(),
        name='meeting-list-create',
    ),
    path(
        'meetings/<int:pk>/',
        MeetingDetailView.as_view(),
        name='meeting-detail',
    ),
]
