from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.engine.app import neo4j_client
from opulence.engine.models.scan import Scan
from uuid import uuid4
from typing import List

def create(scan: Scan):
    neo4j_scans.create(neo4j_client, scan)


def add_facts(scan_id: uuid4, facts_ids: List[uuid4]):
    neo4j_scans.add_facts(neo4j_client, scan_id, facts_ids)
