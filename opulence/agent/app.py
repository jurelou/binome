from typing import List
from celery.signals import worker_init
from config import engine_config
from opulence.agent import celery_app
from opulence.common.base_fact import BaseFact
from opulence.agent.scan import tasks
from opulence.common.database.es import create_indexes

# @celery_app.task(name="scan.launch")
# def launch_scan(collector_name: str, facts: List[BaseFact]):
#     print("!!!!!!aaaaaa", collector_name)
#     print("=====", facts)


@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        create_indexes(engine_config.elasticsearch.endpoint)
    except Exception as err:
        print(f"Error while bootstraping elasticsearch: {err}")

