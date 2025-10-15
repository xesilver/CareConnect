from django.db import models


class SMSMessage(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    ]

    to_number = models.CharField(max_length=32)
    body = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")
    message_sid = models.CharField(max_length=64, blank=True, db_index=True)
    error_code = models.CharField(max_length=32, blank=True)
    error_message = models.TextField(blank=True)
    appointment = models.ForeignKey(
        'core.Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_messages'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SMS Message"
        verbose_name_plural = "SMS Messages"
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"SMS to {self.to_number} [{self.status}]"
