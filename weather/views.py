from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import WeatherSnapshot
from .serializers import WeatherSnapshotSerializer

class WeatherSnapshotViewSet(ReadOnlyModelViewSet):
    queryset = WeatherSnapshot.objects.select_related("venue")
    serializer_class = WeatherSnapshotSerializer
