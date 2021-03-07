from time import time
from typing import List
from uuid import uuid4

from loguru import logger
from opulence.engine.models.scan import Scan


def get_user_input_facts(client, scan_id: uuid4, include_scan=True):
    logger.info(f"Get user input facts from scan {scan_id}")
    with client.session() as session:
        result = session.run(
            "MATCH (scan: Scan)-[link:user_input]->(fact: Fact) "
            "WHERE scan.external_id=$external_id "
            "RETURN DISTINCT fact, scan",
            external_id=scan_id.hex,
        )

        data = result.data()
        scan = data[0]["scan"]
        facts = [(item["fact"]["type"], item["fact"]["external_id"]) for item in data]
    return Scan(**scan), facts


def create(client, scan: Scan):
    logger.info(f"Create scan {scan}")
    with client.session() as session:
        session.run(
            "CREATE (scan:Scan {external_id: $external_id}) " "SET scan += $data",
            external_id=scan.external_id.hex,
            data=scan.dict(exclude={"external_id", "facts"}),
        )


def add_facts(client, scan_id: uuid4, facts_ids: List[str]):
    formated_links = [{"from": scan_id.hex, "to": fact} for fact in facts_ids]
    logger.info(f"Add {len(facts_ids)} facts to {scan_id}")
    with client.session() as session:
        session.run(
            "UNWIND $links as link "
            "MATCH (from:Scan), (to:Fact) "
            "WHERE from.external_id = link.from AND to.external_id = link.to "
            "CREATE (from)-[:user_input {timestamp: $timestamp} ]->(to)",
            links=formated_links,
            timestamp=time(),
        )
