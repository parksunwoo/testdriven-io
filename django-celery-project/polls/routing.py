from django.urls import pathlib
from polls import consumers


urlpatterns = [
    path('ws/task_status/<task_id>/', consumers.TaskStatusConsumer.as_asgi()),
]