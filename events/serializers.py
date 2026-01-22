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

class EventImagesUploadSerializer(serializers.Serializer):
    images = serializers.ImageField(required=False)

    def validate(self, attrs):
        request = self.context["request"]
        files = request.FILES.getlist("images")
        if not files:
            raise serializers.ValidationError(
                {"images": "Upload at least one file using form-data key 'images'."}
            )
        attrs["images"] = files
        return attrs

class EventImagesResponseSerializer(serializers.Serializer):
    preview_image_url = serializers.SerializerMethodField()
    images = EventImageSerializer(many=True)

    def get_preview_image_url(self, obj):
        request = self.context.get("request")
        event = obj["event"]
        if not event.preview_image:
            return None
        url = event.preview_image.url
        return request.build_absolute_uri(url) if request else url
    
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()