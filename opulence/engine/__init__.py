from config import engine_config
from opulence.common.database.es import create_client
from opulence.common.celery import create_celery_app

celery_app = create_celery_app()
celery_app.conf.update(
    {
        'task_routes': {
                'toto.*': { 'queue': 'toto', 'exchange': 'toto' }
        }
    }
)
celery_app.conf.update(engine_config.celery)

es_client = create_client(engine_config.elasticsearch)
