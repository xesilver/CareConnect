from django.test import TestCase
from django.utils import timezone
from django_tenants.utils import tenant_context, schema_context

from tenants.models import Tenant
from .models import Patient, Appointment


class CoreModelsTest(TestCase):
    def setUp(self):
        with schema_context('public'):
            self.tenant = Tenant.objects.create(schema_name="clinic1", name="Clinic 1")

    def test_patient_and_appointment_creation(self):
        with tenant_context(self.tenant):
            patient = Patient.objects.create(
                first_name="Jane",
                last_name="Doe",
                date_of_birth=timezone.now().date(),
                phone_number="+15555550100",
            )
            self.assertEqual(str(patient), "Jane Doe")

            appt = Appointment.objects.create(
                patient=patient,
                scheduled_at=timezone.now(),
                reason="Follow-up",
            )
            self.assertIn("Appointment for", str(appt))

# Create your tests here.
