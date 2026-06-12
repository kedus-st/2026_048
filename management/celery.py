from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clearance.settings')

app = Celery('management')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

CELERY_TIMEZONE = 'Europe/Berlin'

app.conf.beat_schedule = {
    'run-every-day': {
        'task': 'management.tasks.auto_report',
        'schedule': crontab(minute='0', hour='21'),  # Run every day at 9pm / Server 11pm
    },
    
    #'run-every-minute': {
    #    'task': 'management.tasks.celery_test',
    #    'schedule': crontab(minute='*'),  # Run every minute
    #},
}