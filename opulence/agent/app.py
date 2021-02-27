from opulence.common.celery import create_app
from opulence.common.database.es import create_client
from opulence.agent.controllers.collectors import all_collectors

from celery.signals import worker_init
from opulence.config import agent_config
from opulence.common.database.es import create_indexes
from kombu import Queue
from opulence.agent.controllers.collectors import all_collectors


queues = [Queue(collector) for collector in all_collectors.keys()]


# Create celery app
celery_app = create_app()
celery_app.conf.update({
    'collectors': {c_name: {"active": c_item["active"], "config": c_item["instance"].config.dict()} for c_name, c_item in all_collectors.items()},
    'imports': "opulence.agent.tasks",
    'task_queues': queues
})
celery_app.conf.update(agent_config.celery)


# Create ES instance
es_client = create_client(agent_config.elasticsearch)

@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    
    for name, collector in all_collectors.items():
        print(f"{name} -> active: {collector['active']}")

    try:
        create_indexes(es_client)
    except Exception as err:
        logger.error(f"Error while bootstraping elasticsearch: {err}")
    logger.debug("startup finished")
    print("j'ai comence")
