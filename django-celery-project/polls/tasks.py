from celery import shared_task

import logging
import json
import random

import requests
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from polls.consumers import notify_channel_layer
from django.contrib.auth.models import User

from polls.base_task import custom_celery_task


logger = get_task_logger(__name__)


@shared_task()
def sample_task(email):
    from polls.views import api_call

    api_call(email)


# @shared_task(bind=True)
# def task_process_notification(self):
#     try:
#         if not random.choice([0, 1]):
#             raise Exception()
#
#         requests.post('https://httpbin.org/delay/5')
#     except Exception as e:
#         logger.error('exception raised, it would be retry after 5 seconds')
#         raise self.retry(exc=e, countdown=5)


@shared_task(bind=True, auto_retry_for=(Exception, ), retry_kwargs={'max_retries': 7, 'countdown': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        raise Exception()

    requests.post('https://httpbin.org/delay/5')


@shared_task(bind=True, auto_retry_for=(Exception, ), retry_backoff=5, retry_kwargs={'max_retries': 5})
def task_process_notification(self):
    if not random.choice([0, 1]):
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
