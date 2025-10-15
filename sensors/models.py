from django.db import models


class SensorReading(models.Model):
    SENSOR_CHOICES = [
        ("glucometer", "Glucometer"),
        ("bp_cuff", "Blood Pressure Cuff"),
        ("thermometer", "Thermometer"),
        ("spo2", "Pulse Oximeter"),
    ]

    patient = models.ForeignKey('core.Patient', on_delete=models.CASCADE, related_name='sensor_readings')
    sensor_type = models.CharField(max_length=32, choices=SENSOR_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=16)
    measured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sensor Reading"
        verbose_name_plural = "Sensor Readings"
        indexes = [
            models.Index(fields=["measured_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.sensor_type} {self.value}{self.unit} at {self.measured_at}"
