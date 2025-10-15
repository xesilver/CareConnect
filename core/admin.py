from django.contrib import admin
from .models import User, Patient, Appointment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "display_name", "is_staff", "is_active")
    search_fields = ("username", "email", "display_name")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "phone_number")
    search_fields = ("first_name", "last_name", "phone_number")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "scheduled_at", "reason")
    list_filter = ("scheduled_at",)

# Register your models here.
