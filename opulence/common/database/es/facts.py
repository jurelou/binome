from elasticsearch.helpers import bulk

from opulence.common.fact import all_facts
from uuid import uuid4
from typing import List

replicas = 0
refresh_interval = "3s"

gen_index_name = lambda name: f"facts_{name.lower()}"

# def _refresh_indexes(client):
#     indexes = ";".join([ gen_index_name(fact) for fact in all_facts.keys() ])
#     print("@@@@", indexes)

#     client.indices.refresh(index=indexes, allow_no_indices=True)


def create_indexes(client):
    for fact, body in all_facts.items():
        index_name = gen_index_name(fact)
        client.indices.create(
            index=index_name, body=body.elastic_mapping(), ignore=400,
        )
        client.indices.put_settings(
            index=index_name,
            body={"refresh_interval": refresh_interval, "number_of_replicas": replicas},
        )


def remove_indexes(client):
    for fact in all_facts.keys():
        index_name = gen_index_name(fact)
        print(f"Remove index {index_name}")
        client.indices.delete(index=index_name, ignore=[404])


def bulk_upsert(client, facts):
    def gen_actions(facts):
        for fact in facts:
            yield {
                "_op_type": "update",
                "_index": gen_index_name(fact.schema()["title"]),
                "_id": fact.hash__,
                "upsert": fact.dict(exclude={"hash__"}),
                "doc": fact.dict(exclude={"first_seen", "hash__"}),
            }
            print("Upsert to", gen_index_name(fact.schema()["title"]))

    bulk(client=client, actions=gen_actions(facts))


def get_many(client, facts: List[uuid4]):
    mapping = {}
    for fact_id, fact_type in facts:
        if fact_type not in mapping:
            mapping[fact_type] = [fact_id]
        else:
            mapping[fact_type].append(fact_id)

    result = []
    for fact_type in mapping.keys():
        res = client.mget(index=gen_index_name(fact_type), body = {'ids': mapping[fact_type]})
        for r in res["docs"]:
            result.append(r["_source"])
    return result
