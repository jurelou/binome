from typing import List
from celery.signals import worker_init
from config import agent_config
from opulence.agent import celery_app
from opulence.common.fact import BaseFact
from opulence.agent import tasks
from opulence.common.database.es import create_indexes
from opulence.engine import es_client

# @celery_app.task(name="scan.launch")
# def launch_scan(collector_name: str, facts: List[BaseFact]):
#     print("!!!!!!aaaaaa", collector_name)
#     print("=====", facts)


@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        create_indexes(es_client)
    except Exception as err:
        print(f"Error while bootstraping elasticsearch: {err}")
