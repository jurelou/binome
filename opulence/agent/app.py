from typing import List
from celery.signals import worker_init
from celery.signals import after_setup_logger
from opulence.config import agent_config
from opulence.agent import celery_app
from opulence.common.fact import BaseFact
from opulence.agent import tasks
from opulence.common.database.es import create_indexes
from opulence.agent import es_client
from opulence.common.celery import setup_loggers
import logging

logger = logging.getLogger(__name__)
# @celery_app.task(name="scan.launch")
# def launch_scan(collector_name: str, facts: List[BaseFact]):
#     print("!!!!!!aaaaaa", collector_name)
#     print("=====", facts)


@worker_init.connect
def startup(sender=None, conf=None, **kwargs):
    try:
        create_indexes(es_client)
    except Exception as err:
        logger.error(f"Error while bootstraping elasticsearch: {err}")
    logger.debug("startup finished")

@after_setup_logger.connect
def after_setup_loggers(logger, *args, **kwargs):
    setup_loggers(logger, *args, **kwargs)
