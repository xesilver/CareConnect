from django.contrib import admin
from .models import SMSMessage


@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ("to_number", "status", "message_sid", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("to_number", "message_sid", "body")
