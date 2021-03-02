from typing import List
from uuid import uuid4

from opulence.common.fact import BaseFact


def add_many(client, facts: List[BaseFact]):
    formated_facts = [
        {"external_id": fact.hash__, "data": {"type": fact.schema()["title"]}}
        for fact in facts
    ]

    with client.session() as session:
        session.run(
            "UNWIND $facts as row "
            "MERGE (fact:Fact {external_id: row.external_id}) "
            "ON CREATE SET fact += row.data",
            facts=formated_facts,
        )
