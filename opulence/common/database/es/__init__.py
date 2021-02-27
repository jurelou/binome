from opulence.common.database.es.fact import FactIndex
from elasticsearch import Elasticsearch

import logging

logger = logging.getLogger(__name__)

fact_index = FactIndex()
INDEXES = [fact_index]

def create_client(config):
    logger.info(f"Create elasticsearch client: {config.endpoint}")
    return Elasticsearch(hosts=[config.endpoint])

def create_indexes(es_client):
    for index in INDEXES:
        if not es_client.indices.exists(index=index.index_name):
            index.create_index(es_client)
            logger.info(f"Created elasticsearch index {index.index_name}")
        else:
            logger.info(f"Index {index.index_name} already exists")


def clean(es_client):
    for index in INDEXES:
        if es_client.indices.exists(index=index.index_name):
            index.remove_index()
            logger.info(f"Remove index {index.index_name}")
