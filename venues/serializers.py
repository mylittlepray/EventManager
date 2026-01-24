# venues/serializers.py
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField() 

    class Meta:
        model = Venue
        fields = ['id', 'name', 'location']

    @extend_schema_field({'type': 'object', 'example': {'type': 'Point', 'coordinates': [92.8526, 56.0106]}})
    def get_location(self, obj):
        if obj.location:
            return {"latitude": obj.location.y, "longitude": obj.location.x}
        return None
