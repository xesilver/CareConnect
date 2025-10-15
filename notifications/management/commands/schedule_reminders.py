from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_tenants.utils import tenant_context, get_tenant_model
from core.models import Appointment
from notifications.models import SMSMessage
from notifications.tasks import send_sms_task


class Command(BaseCommand):
    help = "Find appointments 24h ahead and queue SMS reminders for each tenant"

    def handle(self, *args, **options):
        Tenant = get_tenant_model()
        now = timezone.now()
        window_start = now + timedelta(hours=24)
        window_end = now + timedelta(hours=25)

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
        self.stdout.write(self.style.SUCCESS("Scheduled reminders queued"))


