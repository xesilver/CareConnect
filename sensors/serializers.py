from rest_framework import serializers
from .models import SensorReading


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['id', 'patient', 'sensor_type', 'value', 'unit', 'measured_at', 'created_at']

