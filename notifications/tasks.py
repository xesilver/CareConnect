from celery import shared_task
from django.conf import settings
from twilio.rest import Client
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

