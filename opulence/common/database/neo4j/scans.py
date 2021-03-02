from typing import List
from uuid import uuid4
from time import time
from opulence.engine.models.scan import Scan

# def get_(client, scan_id: uuid4) -> Scan:
#     with client.session() as session:
#         scan = session.run(
#                 "MATCH (scan: Scan) "
#                 "WHERE scan.external_id=$external_id "
#                 "RETURN DISTINCT scan",
#                 external_id=scan_id.hex
#         )
#         scan = scan.single().data()["scan"]
#     return Scan(**scan)

def get_user_input_facts(client, scan_id: uuid4, include_scan=True):
    with client.session() as session:
        result = session.run(
                "MATCH (scan: Scan)-[link:user_input]->(fact: Fact) "
                "WHERE scan.external_id=$external_id "
                "RETURN DISTINCT fact, scan",
                external_id=scan_id.hex
        )
        # print("@@@@", scan.values())

        data = result.data()
        scan = data[0]["scan"]
        facts = [ (item["fact"]["external_id"], item["fact"]["type"]) for item in data ]
    return Scan(**scan), facts


def create(client, scan: Scan):
    with client.session() as session:
        session.run(
            "CREATE (scan:Scan {external_id: $external_id}) " "SET scan += $data",
            external_id=scan.external_id.hex,
            data=scan.dict(exclude={"external_id", "facts"}),
        )


def add_facts(client, scan_id: uuid4, facts_ids: List[str]):
    formated_links = [{"from": scan_id.hex, "to": fact} for fact in facts_ids]

    with client.session() as session:
        session.run(
            "UNWIND $links as link "
            "MATCH (from:Scan), (to:Fact) "
            "WHERE from.external_id = link.from AND to.external_id = link.to "
            "CREATE (from)-[:user_input {timestamp: $timestamp} ]->(to)",
            links=formated_links,
            timestamp=time()
        )
