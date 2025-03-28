import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HW_skypro_Django_REST_Framework.settings")

app = Celery("HW_skypro_Django_REST_Framework")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
