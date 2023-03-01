from unittest import mock

import pytest
import requests
from celery.exceptions import Retry

from polls.tasks import task_add_subscribe


def test_post_succeed(db, monkeypatch, user):
    mock_request_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_request_post)

    task_add_subscribe(user.pk)

    mock_request_post.assert_called_with(
        'https://httpbin.org/delay/5',
        json={'email': user.email}
    )


def test_exception(db, monkeypatch, user):
    mock_request_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_request_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, 'retry', mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_request_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.pk)
