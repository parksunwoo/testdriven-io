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


# @shared_task(bind=True, auto_retry_for=(Exception, ), retry_kwargs={'max_retries': 7, 'countdown': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         raise Exception()
#
#     requests.post('https://httpbin.org/delay/5')


# @shared_task(bind=True, auto_retry_for=(Exception, ), retry_backoff=5, retry_jitter=True, retry_kwargs={'max_retries': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         raise Exception()
#
#     requests.post('https://httpbin.org/delay/5')


class BaseTaskWithRetry(celery.Task):
    autoretry_fro = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    raise Exception()


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    notify_channel_layer(task_id)


@shared_task(name='task_clear_session')
def task_clear_session():
    from django.core.management import call_command
    call_command('clearsessions')


@shared_task(name='defalt:dynamic_example_one')
def dynamic_example_one():
    logger.info('Example one')


@shared_task(name='low_priority:dynamic_example_two')
def dynamic_example_two():
    logger.info('Example two')


@shared_task(name='high_priority:dynamic_example_three')
def dynamic_example_three():
    logger.info('Example three')


@shared_task()
def task_send_welcome_email(user_pk):
    user = User.objects.get(id=user_pk)
    logger.info(f'send email to {user.email} {user.pk}')


@shared_task()
def task_test_logger():
    logger.info('test')


@shared_task(bind=True)
def task_add_subscribe(self, user_pk):
    try:
        user = User.objects.get(id=user_pk)
        requests.post(
            'https://httpbin.org/delay/5',
            data={'email': user.email}
        )
    except Exception as exec:
        raise self.retry(exc=exec)


@custom_celery_task(max_retries=3)
def task_transaction_test():
    from .views import random_username
    username = random_username()
    user = User.objects.create_user(username=username, 'lennon@thebeats.com', 'johnpassword')
    user.save()
    logger.info(f'send email to {user.pk}')
    raise Exception('test')


