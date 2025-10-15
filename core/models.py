from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    display_name = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        indexes = [
            models.Index(fields=["scheduled_at"]),
        ]

    def __str__(self) -> str:
        return f"Appointment for {self.patient} at {self.scheduled_at}"
