from opulence.common.database.es.facts import FactsIndexes
from opulence.common.database.es import all_indexes
from elasticsearch import Elasticsearch
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import httpx


def create_client(config):
    logger.info(f"Create elasticsearch client: {config.endpoint}")
    return Elasticsearch(hosts=[config.endpoint])

def create_indexes(es_client):
    for index in all_indexes:
        if not es_client.indices.exists(index=index.index_name):
            index.create_index(es_client)
            logger.info(f"Created elasticsearch index {index.index_name}")
        else:
            logger.info(f"Index {index.index_name} already exists")


def remove_indexes(es_client):
    for index in all_indexes:
        if es_client.indices.exists(index=index.index_name):
            index.remove_index(es_client)
            logger.info(f"Remove index {index.index_name}")

def create_kibana_indexes(es_client, kibana_url):
    def _create_index(index_pattern):
        kibana_endpoint = f"{kibana_url}/api/saved_objects/index-pattern/{index_pattern}"
        headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
        data = {
            "attributes": {
            "title": index_pattern
            }
        }
        r = httpx.post(kibana_endpoint, json=data, headers=headers)
        print(f"Kibana create index pattern ({index_pattern}): {r.status_code}")

    _create_index("facts_*")  
    for index in all_indexes:
        _create_index(index.index_name)
