# CareConnect

A modern, multi-tenant telehealth platform built with Django 5, PostgreSQL, Celery, and Twilio.

## Quickstart

1. Create env file

```bash
cp .env.example .env
```

2. (Optional) Use Docker for local services

```bash
docker compose up -d db redis
```

3. Create a virtual environment and install deps

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

4. Create Django project

```bash
python -m django startproject careconnect .
```

5. Run migrations

```bash
python manage.py migrate
python manage.py runserver
```

## AI Development (Cursor)

See `.cursorconfig` for prompts, linter, and commit generation workflow.

## Phases
- Phase 1: Project scaffolding & multi-tenant setup
- Phase 2: Twilio SMS reminders with Celery + webhook tracking
- Phase 3: IoT sensor API (DRF) with token auth

## License
MIT
