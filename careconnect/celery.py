import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careconnect.settings")

app = Celery("careconnect")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


