from config import engine_config
from celery import Celery
from kombu.serialization import register
from opulence.common import json_encoder
from opulence.common.database.es import create_client

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
        'task_routes': {
                # 'scan.*': { 'queue': 'scan', 'exchange': 'scan' }
        },
        "accept_content": ["customEncoder", "application/json"],
        "task_serializer": "customEncoder",
        "result_serializer": "customEncoder",
    }
)
celery_app.conf.update(engine_config.celery)

es_client = create_client(engine_config.elasticsearch)