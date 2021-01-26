from opulence.common.database.es import facts_index
from elasticsearch import Elasticsearch



INDEXES = [facts_index]

def create_client(config):
    print("GO", config.endpoint)
    return Elasticsearch(hosts=[config.endpoint])

def create_indexes(es_client):
    print("Bootstraping elasticsearch indexes")
    for index in INDEXES:
        if not es_client.indices.exists(index=index.index_name):
            index.create_index()
            print("finish")
        else:
            print(f"Index {index.index_name} already exists")
    print("done")


# def clean(es_client):
#     for index in indexes:
#         if es_client.indices.exists(index=index.index_name):
#             print(f"Remove index {index.index_name}")
#             index.remove_index()
