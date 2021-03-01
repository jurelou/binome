from celery.signals import worker_init, worker_ready
from celery.result import allow_join_result

from opulence.common.celery import create_app
from opulence.common.database.es import utils as es_utils
from opulence.config import engine_config

from opulence.common.database.neo4j import utils as neo4j_utils 

# Create celery app
celery_app = create_app()
celery_app.conf.update(engine_config.celery)

celery_app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "opulence.engine.tasks.reload_agents",
        "schedule": engine_config.refresh_agents_interval,
    },
}
celery_app.conf.update({"imports": "opulence.engine.tasks"})

es_client = es_utils.create_client(engine_config.elasticsearch)
neo4j_client = neo4j_utils.create_client(engine_config.neo4j)



@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    try:

        es_utils.remove_indexes(es_client)
        es_utils.create_indexes(es_client)

        # es_utils.remove_kibana_patterns(es_client, kibana_url=engine_config.kibana.url)
        es_utils.create_kibana_patterns(es_client, kibana_url=engine_config.kibana.url)


        neo4j_utils.flush(neo4j_client)
        neo4j_utils.create_constraints(neo4j_client)


    except Exception as err:
        print(f"ERROR in worker_init signal {err}")




@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    from opulence.engine.models.scan import Scan
    from opulence.engine.models.case import Case
    from opulence.engine import tasks  # pragma: nocover
    from opulence.facts.person import Person
    case = Case()
    scan = Scan(collector_name="lol", facts=[Person(firstname="fname", lastname="lname")])
    tasks.add_case.apply(args=[case])
    print("Now adding scan")
    tasks.add_scan.apply(args=[case.external_id, scan])
    