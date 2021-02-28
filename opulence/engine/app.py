from opulence.config import engine_config
from opulence.common.celery import create_app

from celery.signals import worker_init
from opulence.common.database.es import utils as es_utils

# Create celery app
celery_app = create_app()
celery_app.conf.update(engine_config.celery)

celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'opulence.engine.tasks.reload_agents',
        'schedule': engine_config.refresh_agents_interval
    },
}
celery_app.conf.update({'imports': "opulence.engine.tasks"})

es_client = es_utils.create_client(engine_config.elasticsearch)


from opulence.engine import tasks # pragma: nocover
tasks.scan.delay()


@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        # es_utils.remove_kibana_patterns(es_client, kibana_url=engine_config.kibana.url)
        es_utils.create_kibana_patterns(es_client, kibana_url=engine_config.kibana.url)

        es_utils.remove_indexes(es_client)
        es_utils.create_indexes(es_client)

    except Exception as err:
        print(f"ERROR in worker_init signal {err}")
    # try:
    #     create_indexes(es_client)
    # except Exception as err:
    #     logger.error(f"Error while bootstraping elasticsearch: {err}")
