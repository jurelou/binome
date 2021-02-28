from elasticsearch.helpers import bulk

from opulence.common.fact import all_facts

replicas = 0
refresh_interval = "30s"

gen_index_name = lambda name: f"facts_{name.lower()}"

def create_indexes(es_client):
    for fact, body in all_facts.items():
        index_name = gen_index_name(fact)
        es_client.indices.create(index=index_name, body=body.elastic_mapping(), ignore=400)
        es_client.indices.put_settings(
            index=index_name,
            body={"refresh_interval": refresh_interval, "number_of_replicas": replicas},
        )

def remove_indexes(es_client):
    for fact in all_facts.keys():
        index_name = gen_index_name(fact)
        print(f"Remove index {index_name}")
        es_client.indices.delete(index=index_name, ignore=[404])


def bulk_upsert(es_client, facts):
    def gen_actions(facts):
        for fact in facts:
            yield {
                '_op_type': 'update',
                '_index': gen_index_name(fact.schema()["title"]),
                '_id': fact.hash__,
                'doc': fact.dict(exclude={"hash__"}),
                'doc_as_upsert': True
            }
            print("Upsert to", gen_index_name(fact.schema()["title"]))
    return bulk(client=es_client, actions=gen_actions(facts))
