# venues/views.py
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsSuperUser
from .models import Venue
from .serializers import VenueSerializer

class VenueViewSet(ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsSuperUser]
