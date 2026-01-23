# events/serializers.py
from rest_framework import serializers
from .models import Event, EventImage

from venues.serializers import VenueSerializer
from weather.serializers import WeatherSnapshotSerializer

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["id", "image", "created_at"]


class EventListSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title", 
            "description", 
            "publish_at", 
            "start_at", 
            "end_at", 
            "venue", 
            "rating", 
            "preview_image"
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    weather = WeatherSnapshotSerializer(read_only=True) # Погода
    images = EventImageSerializer(many=True, read_only=True) # Картинки

    class Meta:
        model = Event
        fields = [
            "id",
            "title", 
            "description", 
            "publish_at", 
            "start_at", 
            "end_at", 
            "venue", 
            "rating", 
            "preview_image",
            "status",      # Добавим статус (админу полезно)
            "author",      # Автора
            "weather",     # <-- Добавлено
            "images",      # <-- Добавлено
        ]

    def to_representation(self, instance):
        """
        Динамическое скрытие полей для обычных пользователей.
        Если юзер НЕ суперюзер, убираем системные поля, но оставляем weather/images.
        """
        rep = super().to_representation(instance)
        request = self.context.get('request')

        # Если пользователь НЕ суперюзер (или аноним)
        if not request or not request.user.is_superuser:
            # Можно удалить лишние поля, которые видит только админ
            # Например, если 'status' или 'author' не должны видеть обычные юзеры:
            if 'status' in rep: rep.pop('status')
            if 'author' in rep: rep.pop('author')
            
            # Weather и Images остаются, как ты и просил для "retrieve"
            
        return rep

class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["author", "weather", "preview_image", "rating"] 

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