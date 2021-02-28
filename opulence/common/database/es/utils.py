from elasticsearch import Elasticsearch
from opulence.common.database.es import facts
from celery.utils.log import get_task_logger
from opulence.common.fact import all_facts
import httpx

logger = get_task_logger(__name__)




kibana_index_patterns = ["facts_*"]
kibana_index_patterns.extend([ facts.gen_index_name(index) for index in all_facts.keys()])


def create_client(config):
    logger.info(f"Create elasticsearch client: {config.endpoint}")
    return Elasticsearch(hosts=[config.endpoint])


def create_indexes(es_client):
    facts.create_indexes(es_client)


def remove_indexes(es_client):
    facts.remove_indexes(es_client)


def create_kibana_patterns(es_client, kibana_url):
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

    [ _create_index(index) for index in kibana_index_patterns ]

def remove_kibana_patterns(es_client, kibana_url):
    def _delete_index(index_pattern):
        kibana_endpoint = f"{kibana_url}/api/saved_objects/index-pattern/{index_pattern}"
        r = httpx.delete(kibana_endpoint, headers={"kbn-xsrf": "yes"})
        print(f"Kibana delete index pattern ({index_pattern}): {r.status_code}")

    [ _delete_index(index) for index in kibana_index_patterns ]
