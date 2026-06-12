import datetime
from celery import shared_task
from .models import Report

@shared_task
def auto_report():
    new_report = Report()
    new_report.save()

@shared_task
def celery_test():
    new_report = Report()
    new_report.save()
    print("Celery trigger")