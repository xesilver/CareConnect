# CareConnect Overview

CareConnect is a multi-tenant telehealth platform for healthcare providers (clinics, hospitals) to manage patients, appointments, and automated communications. Each provider operates in an isolated PostgreSQL schema, ensuring strong data separation and easier scaling.

## Purpose

- Enable clinics to run their own secure environment under a unique domain/subdomain
- Simplify patient and appointment management
- Automate high-volume SMS reminders and track delivery outcomes
- Optionally ingest IoT sensor data for remote patient monitoring

## Core Features

- Multi-tenancy (schema-per-tenant) via `django-tenants`
- Patient and appointment models with basic admin UX
- Asynchronous SMS reminders with Twilio (Celery + Redis)
- Delivery tracking webhook and dashboard API
- IoT sensor ingestion API (DRF) secured via token auth

## Architecture

- Backend: Django 5, Django REST Framework
- Multi-tenancy: `django-tenants` (public schema + one schema per tenant)
- Database: PostgreSQL (single DB, multiple schemas)
- Background jobs: Celery with Redis broker
- SMS: Twilio Python SDK
- Container/dev services: Docker Compose (Postgres, Redis)

### Tenancy Model

- Public schema: holds `tenants.Tenant` and `tenants.Domain`
- Tenant schema: holds app data (users, patients, appointments, notifications, sensors)
- Domain routing: requests are routed to tenant schemas based on `Host` header

## Data Model (High-level)

- `core.User`: Custom user model (per-tenant)
- `core.Patient`: Patient record with basic demographics and phone
- `core.Appointment`: Scheduled appointment linked to a patient
- `notifications.SMSMessage`: Outbound SMS log with status/lifecycle fields
- `sensors.SensorReading`: IoT data points for remote monitoring

## SMS Reminder Workflow

1) Scheduler (Celery beat) runs every 15 minutes
2) For each tenant, find appointments occurring ~24h ahead
3) Create `SMSMessage` records and enqueue `send_sms_task`
4) Twilio webhook updates message status (sent/delivered/failed)

Endpoints
- Webhook: `POST /twilio/webhook/` (Twilio status callbacks)
- Dashboard API: `GET /api/v1/sms/` (auth required)

## IoT Sensor API

- `POST /api/v1/readings/` to create a reading (Token auth)
- `GET /api/v1/readings/` to list readings (Token auth)

Payload example (create):
```json
{
  "patient": 1,
  "sensor_type": "glucometer",
  "value": "100.5",
  "unit": "mg/dL",
  "measured_at": "2025-01-01T10:00:00Z"
}
```

## Local Development

1) Services: `docker compose up -d db redis`
2) Env: app loads `config/local.env` automatically
3) Migrations (public): `python manage.py migrate_schemas --shared`
4) Create a tenant and domain for `localhost`
5) Migrations (tenants): `python manage.py migrate_schemas`
6) Superuser (tenant): `python manage.py tenant_command createsuperuser --schema=<schema>`
7) Run server: `python manage.py runserver`
8) Celery: run worker and beat in separate terminals

## Security Notes

- Data isolation per schema; no cross-tenant joins
- Auth via Django auth (admin) and DRF TokenAuthentication (APIs)
- Webhook endpoint open to Twilio; validate SID/status origin if enabling in production

## Deployment (Scaffolded)

- Terraform scaffold for VPC, S3, ECR (Elastic Beanstalk/RDS planned)
- CI workflow set to manual to avoid accidental provisioning during development

## Roadmap

- Provider-facing UI for appointment workflows
- Role-based access control and audit logging
- S3-backed media/static, production-ready settings and HTTPS
- Observability (logging, tracing), retries with dead-letter queues

