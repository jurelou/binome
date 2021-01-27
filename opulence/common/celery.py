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

def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # FileHandler
    fh = logging.FileHandler('logs.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # SysLogHandler
    #slh = logging.handlers.SysLogHandler(address=('logsN.papertrailapp.com', '...'))
    #slh.setFormatter(formatter)
    #logger.addHandler(slh)
