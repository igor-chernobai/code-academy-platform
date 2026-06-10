from os import environ

from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'academy.settings')

app = Celery('academy', broker='redis://redis:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
