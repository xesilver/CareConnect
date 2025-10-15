from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django_tenants.utils import tenant_context, schema_context

from tenants.models import Tenant, Domain
from core.models import User, Patient
from .models import SensorReading


class SensorsAPITests(TestCase):
    def setUp(self):
        with schema_context('public'):
            self.tenant = Tenant.objects.create(schema_name="clinic1", name="Clinic 1")
        Domain.objects.create(domain="testserver", tenant=self.tenant, is_primary=True)
        with tenant_context(self.tenant):
            self.user = User.objects.create_user(username="api", password="p")
            self.token = Token.objects.create(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
            self.patient = Patient.objects.create(first_name="P", last_name="Q", date_of_birth=timezone.now().date(), phone_number="+1")

    def test_create_and_list_readings(self):
        url = reverse('sensorreading-list-create')
        payload = {
            "patient": self.patient.id,
            "sensor_type": "glucometer",
            "value": "100.5",
            "unit": "mg/dL",
            "measured_at": timezone.now().isoformat(),
        }
        resp = self.client.post(url, data=payload, format='json', HTTP_HOST="testserver")
        self.assertEqual(resp.status_code, 201)
        resp2 = self.client.get(url, HTTP_HOST="testserver")
        self.assertEqual(resp2.status_code, 200)
        self.assertGreaterEqual(len(resp2.json()), 1)

# Create your tests here.
