from opulence.config import engine_config
from opulence.common.database.es import create_client, INDEXES
from opulence.common.celery import create_app
import httpx
import logging

logger = logging.getLogger(__name__)
# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        'task_routes': {
                # 'scan.*': { 'queue': 'scan', 'exchange': 'scan' }
        }
    }
)
celery_app.conf.update(engine_config.celery)

# Create ES instance
es_client = create_client(engine_config.elasticsearch)

# Create kibana defaut index patterns
for index in INDEXES:
    kibana_endpoint = f"{engine_config.kibana.url}/api/saved_objects/index-pattern/{index.index_name}"
    headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
    data = {
        "attributes": {
        "title": f"{index.index_name}*"
        }
    }
    r = httpx.post(kibana_endpoint, json=data, headers=headers)
    logger.info(f"Kibana create index pattern ({index}): {r.status_code}")
