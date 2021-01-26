from opulence.common.database.es.fact import FactIndex
from elasticsearch import Elasticsearch



INDEXES = [FactIndex()]

def create_client(config):
    print(f"Create ES client for config: {config.endpoint}")
    return Elasticsearch(hosts=[config.endpoint])

def create_indexes(es_client):
    print("Bootstraping elasticsearch indexes")
    for index in INDEXES:
        if not es_client.indices.exists(index=index.index_name):
            index.create_index()
            print("finish")
        else:
            print(f"Index {index.index_name} already exists")


# def clean(es_client):
#     for index in indexes:
#         if es_client.indices.exists(index=index.index_name):
#             print(f"Remove index {index.index_name}")
#             index.remove_index()
