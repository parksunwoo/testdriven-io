
import os
import logging

from celery import Celery
from celery.signals import after_setup_logger

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_example.settings')

app = Celery('django_celery_example')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodicover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def divide(x, y):
    import time
    time.sleep(10)
    return x / y

@after_setup_logger.connect()
def on_after_setup_logger(logger, **kwargs):
    formatter = logger.handlers[0].formatter
    file_handler = logging.FileHandler('celery.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)