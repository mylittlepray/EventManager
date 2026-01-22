# events/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsSuperUserOrReadOnly
from .models import Event, EventImage, EventStatus
from .serializers import EventSerializer, EventImageSerializer, EventImagesUploadSerializer, EventImagesResponseSerializer
from .utils import make_preview
from .filters import EventFilter

class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filterset_class = EventFilter

    search_fields = [
        "title",
        "venue__name",
    ]

    ordering_fields = [
        "title",
        "start_at",
        "end_at",
    ]
    ordering = ["start_at"] 

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

    def get_serializer_class(self):
        if self.action == "images_upload":
            return EventImagesUploadSerializer
        return super().get_serializer_class()

    @action(
        detail=True,
        methods=[],
        url_path="images",
        parser_classes=[MultiPartParser, FormParser],
    )
    def images(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @images.mapping.get
    def images_list(self, request, pk=None):
        event = self.get_object()
        qs = event.images.all().order_by("-created_at")

        payload = {"event": event, "images": qs}
        data = EventImagesResponseSerializer(payload, context={"request": request}).data
        return Response(data)

    @images.mapping.post
    def images_upload(self, request, pk=None):
        event = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        files = serializer.validated_data["images"]

        created = []
        for f in files:
            created.append(EventImage.objects.create(event=event, image=f))

        if not event.preview_image and created:
            first = created[0]
            first.image.open("rb")
            preview_content = make_preview(first.image.file, min_side=200)
            event.preview_image.save(
                f"event_{event.id}_preview.jpg",
                preview_content,
                save=True,
            )

        return Response(
            EventImageSerializer(created, many=True, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )