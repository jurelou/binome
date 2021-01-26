from config import engine_config
from celery.signals import worker_init

from opulence.engine import celery_app
from opulence.engine.agent_manager import Manager
from opulence.common.database.es import create_indexes
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
    except Exception as err:
        print(f"Error while bootstraping elasticsearch: {err}")



from opulence.agent import signatures
from opulence.facts.person import Person
a = signatures.launch_scan("b-collector", [Person(firstname="lol", lastname="mdr")]).delay()
print("!!!!!!!!!!!", a.get())
