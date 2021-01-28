from config import agent_config

from opulence.common.celery import create_app
from opulence.common.database.es import create_client
from opulence.agent.collectors import all_collectors



# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        'collectors': {c_name: {"active": c_item["active"], "config": c_item["instance"].config.dict()} for c_name, c_item in all_collectors.items()},
        'task_routes': {
                'scan.*': { 'queue': 'scan', 'exchange': 'scan' }
        },
    }
)
celery_app.conf.update(agent_config.celery)


# Create ES instance
es_client = create_client(agent_config.elasticsearch)
