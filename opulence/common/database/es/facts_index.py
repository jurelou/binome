index_name = "facts"

def get_elastic_mapping():
        return {"mappings": {"properties": {}}}

def create_index(es_client):
    es_client.indices.create(index=index_name)
    es_client.indices.put_settings(
        index=index_name,
        body={"refresh_interval": "30s", "number_of_replicas": 0},
    )

def remove_index(es_client):
    es_client.indices.delete(index=index_name)

def toto():
    pass