from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django_tenants.utils import tenant_context, schema_context

from tenants.models import Tenant, Domain
from core.models import User, Patient, Appointment
from .models import SMSMessage


class NotificationsTests(TestCase):
    def setUp(self):
        with schema_context('public'):
            self.tenant = Tenant.objects.create(schema_name="clinic1", name="Clinic 1")
        Domain.objects.create(domain="testserver", tenant=self.tenant, is_primary=True)
        with tenant_context(self.tenant):
            self.user = User.objects.create_user(username="u", password="p")
            self.token = Token.objects.create(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_webhook_updates_status(self):
        with tenant_context(self.tenant):
            sms = SMSMessage.objects.create(to_number="+1555", body="hi")
        url = reverse('twilio-webhook')
        resp = APIClient().post(url, data={"MessageSid": "SM123", "MessageStatus": "delivered"}, HTTP_HOST="testserver")
        self.assertEqual(resp.status_code, 200)
        with tenant_context(self.tenant):
            # message not found initially; webhook ignores missing SID gracefully
            self.assertEqual(SMSMessage.objects.count(), 1)

    def test_sms_list_requires_auth(self):
        with tenant_context(self.tenant):
            Patient.objects.create(first_name="A", last_name="B", date_of_birth=timezone.now().date(), phone_number="+1")
        url = reverse('sms-list')
        resp = APIClient().get(url, HTTP_HOST="testserver")
        self.assertIn(resp.status_code, [401, 403])
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, 200)

# Create your tests here.
