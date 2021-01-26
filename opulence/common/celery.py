from celery import Celery
from kombu.serialization import register
from opulence.common import json_encoder


def create_app():
  register(
      "customEncoder",
      json_encoder.json_dumps,
      json_encoder.json_loads,
      content_type="application/x-customEncoder",
      content_encoding="utf-8",
  )
  celery_app = Celery(__name__)
  celery_app.conf.update(
      {
          "accept_content": ["customEncoder", "application/json"],
          "task_serializer": "customEncoder",
          "result_serializer": "customEncoder",
      }
  )
  return celery_app  
