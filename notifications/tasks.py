from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django_tenants.utils import tenant_context, get_tenant_model
from twilio.rest import Client
from core.models import Appointment
from .models import SMSMessage


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, max_retries=3)
def send_sms_task(self, sms_id: int) -> str:
    sms = SMSMessage.objects.get(pk=sms_id)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=sms.to_number,
        from_=settings.TWILIO_FROM_NUMBER,
        body=sms.body,
        status_callback=settings.ALLOWED_HOSTS and f"https://{settings.ALLOWED_HOSTS[0]}/twilio/webhook/" or None,
    )
    sms.message_sid = message.sid
    sms.status = "sent"
    sms.save(update_fields=["message_sid", "status", "updated_at"])
    return sms.message_sid


@shared_task
def queue_24h_reminders_task() -> int:
    Tenant = get_tenant_model()
    now = timezone.now()
    window_start = now + timedelta(hours=24)
    window_end = now + timedelta(hours=25)
    queued = 0
    for tenant in Tenant.objects.all():
        with tenant_context(tenant):
            appts = Appointment.objects.filter(
                scheduled_at__gte=window_start, scheduled_at__lt=window_end
            ).select_related('patient')
            for appt in appts:
                body = f"Reminder: appointment on {appt.scheduled_at:%Y-%m-%d %H:%M}."
                sms = SMSMessage.objects.create(
                    to_number=appt.patient.phone_number,
                    body=body,
                    appointment=appt,
                    status="queued",
                )
                send_sms_task.delay(sms.id)
                queued += 1
    return queued

