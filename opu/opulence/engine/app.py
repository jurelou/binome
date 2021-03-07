from celery.result import allow_join_result
from celery.signals import worker_init
from celery.signals import worker_ready
from loguru import logger

from opulence.common.celery import create_app
from opulence.common.database.es import utils as es_utils
from opulence.common.database.neo4j import utils as neo4j_utils
from opulence.config import engine_config


# Create celery app
celery_app = create_app()
celery_app.conf.update(engine_config.celery)

celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'opulence.engine.tasks.reload_agents',
        'schedule': engine_config.refresh_agents_interval,
    },
}
celery_app.conf.update({'imports': 'opulence.engine.tasks'})

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
        logger.critical(f'Error in signal `worker_init`: {err}')


@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    try:
        from opulence.engine.models.case import Case
        from opulence.engine.models.scan import Scan
        from opulence.engine import tasks  # pragma: nocover
        from opulence.facts.person import Person

        case = Case()
        # scan = Scan(collector_name="lol", facts=[Person(firstname="fname", lastname="lname")])
        scan = Scan(
            scan_type='simplescan',
            facts=[
                Person(firstname='fname222', lastname='lname22'),
                Person(firstname='fname', lastname='lname', first_seen=1, last_seen=100),
                Person(
                    firstname='fname',
                    lastname='lname',
                    anther='ldm',
                    first_seen=42,
                    last_seen=200,
                ),
            ],
        )

        tasks.add_case.apply(args=[case])     
        tasks.add_scan.apply(args=[case.external_id, scan])
        tasks.launch_scan.apply(args=[scan.external_id])
    except Exception as err:
        logger.critical(f"Error in signal `worker_ready`: {err}")
