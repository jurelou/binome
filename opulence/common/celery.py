import celery
import logging
from kombu.serialization import register
from opulence.common import json_encoder
import sys

def create_app():
  register(
      "customEncoder",
      json_encoder.json_dumps,
      json_encoder.json_loads,
      content_type="application/x-customEncoder",
      content_encoding="utf-8",
  )
  celery_app = celery.Celery(__name__)
  celery_app.conf.update(
      {
          "accept_content": ["customEncoder", "application/json"],
          "task_serializer": "customEncoder",
          "result_serializer": "customEncoder",
      }
  )
  return celery_app  

def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    print("@@@@@@@@@@@@@")
    # FileHandler
    fh = logging.FileHandler('opulence.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Stdout handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # SysLogHandler
    #slh = logging.handlers.SysLogHandler(address=('logsN.papertrailapp.com', '...'))
    #slh.setFormatter(formatter)
    #logger.addHandler(slh)

def sync_call(app, task_path, timeout=5, **kwargs):
    try:
        task = app.send_task(task_path, **kwargs)
        return task.get(timeout=timeout)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError("{}".format(task_path))


def async_call(app, task_path, **kwargs):
    try:
        return app.send_task(task_path, **kwargs)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError("{}".format(task_path))
