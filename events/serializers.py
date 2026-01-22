# events/serializers.py
from rest_framework import serializers
from .models import Event, EventImage

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["id", "image", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "publish_at",
            "start_at",
            "end_at",
            "author",
            "venue",
            "rating",
            "status",
            "preview_image",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["preview_image", "created_at", "updated_at"]
