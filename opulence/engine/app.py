from config import engine_config
from celery.signals import worker_init

from opulence.engine import celery_app
from opulence.engine.agent_manager import Manager
from opulence.common.database.es import create_kibana_index_patterns, create_indexes
from opulence.engine import es_client
from opulence.engine import tasks # fw declaration ?

Manager()

@celery_app.task(name="engine.toto")
def toto():
    print("!!!!!!ENGINE TOTO")

@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        create_indexes(es_client)
        create_kibana_index_patterns()
    except Exception as err:
        print(f"Error while bootstraping elasticsearch: {err}")

