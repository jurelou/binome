from opulence.common.database.es import facts_index
import httpx
from config import engine_config
from elasticsearch import Elasticsearch



indexes = [facts_index]

def create_client(config):
    print("GO", config.endpoint)
    return Elasticsearch(hosts=[config.endpoint])

def create_indexes(es_client):
    print("Bootstraping elasticsearch indexes")
    for index in indexes:
        if not es_client.indices.exists(index=index.index_name):
            index.create_index()
            print("finish")
        else:
            print(f"Index {index.index_name} already exists")
    print("done")

def create_kibana_index_patterns():
    for index in indexes:
        kibana_endpoint = f"{engine_config.kibana.url}/api/saved_objects/index-pattern/{index.index_name}"
        headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
        data = {
            "attributes": {
                "title": f"{index.index_name}*"
            }
        }
        r = httpx.post(kibana_endpoint, json=data, headers=headers)
        print(f"Kibana create index pattern: {r.status_code}")

# def clean(es_client):
#     for index in indexes:
#         if es_client.indices.exists(index=index.index_name):
#             print(f"Remove index {index.index_name}")
#             index.remove_index()
