from opulence.common.database.neo4j import facts as neo4j_facts
from opulence.common.database.es import facts as es_facts
from opulence.engine.app import neo4j_client, es_client
from typing import List
from opulence.common.fact import BaseFact


def create_many(facts: List[BaseFact]):
    es_facts.bulk_upsert(es_client, facts)
    neo4j_facts.create_many(neo4j_client, facts)
