# events/views.py
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsSuperUserOrReadOnly
from .models import Event, EventStatus
from .serializers import EventSerializer

class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        qs = Event.objects.select_related("venue", "author").prefetch_related("images")
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return qs
        return qs.filter(status=EventStatus.PUBLISHED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.status = EventStatus.DELETED
        instance.save(update_fields=["status"])
