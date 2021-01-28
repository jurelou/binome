from opulence.config import engine_config
from celery.signals import worker_init, after_setup_logger

from opulence.engine import celery_app
from opulence.engine.agent_manager import Manager
from opulence.common.database.es import create_indexes
from opulence.engine import es_client
from opulence.engine import tasks # fw declaration ?
from opulence.common.celery import setup_loggers
import logging

logger = logging.getLogger(__name__)
Manager()

@celery_app.task(name="engine.toto")
def toto():
    print("!!!!!!ENGINE TOTO")

@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        create_indexes(es_client)
    except Exception as err:
        logger.error(f"Error while bootstraping elasticsearch: {err}")

@after_setup_logger.connect
def after_setup_loggers(logger, *args, **kwargs):
    setup_loggers(logger, *args, **kwargs)
