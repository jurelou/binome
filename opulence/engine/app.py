from opulence.config import engine_config
from opulence.common.celery import create_app


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

from opulence.engine import tasks # pragma: nocover
tasks.scan.delay()



import logging

log = logging.getLogger("root")
print("aa===========")
log.debug("bbb=================================")

log.info("cool")