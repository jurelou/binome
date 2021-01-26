from config import engine_config
from opulence.common.database.es import create_client, INDEXES
from opulence.common.celery import create_app
import httpx

# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        'task_routes': {
                'toto.*': { 'queue': 'toto', 'exchange': 'toto' }
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
    print(f"Kibana create index pattern: {r.status_code}")
