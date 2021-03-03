from typing import List
from uuid import uuid4

from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.engine.app import neo4j_client
from opulence.engine.controllers import fact as fact_ctrl
from opulence.engine.models.scan import Scan


def create(scan: Scan):
    neo4j_scans.create(neo4j_client, scan)


def add_facts(scan_id: uuid4, facts_ids: List[uuid4]):
    neo4j_scans.add_facts(neo4j_client, scan_id, facts_ids)


def get(scan_id: uuid4):

    scan, facts = neo4j_scans.get_user_input_facts(neo4j_client, scan_id)
    scan.facts = fact_ctrl.get_many(facts)
    print("!!!!", scan.facts)
    return scan
