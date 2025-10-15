from rest_framework import generics, permissions
from .models import SensorReading
from .serializers import SensorReadingSerializer


class SensorReadingListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SensorReading.objects.all().order_by('-measured_at')
    serializer_class = SensorReadingSerializer
