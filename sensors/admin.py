from django.contrib import admin
from .models import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("patient", "sensor_type", "value", "unit", "measured_at")
    list_filter = ("sensor_type", "measured_at")
    search_fields = ("patient__first_name", "patient__last_name")
