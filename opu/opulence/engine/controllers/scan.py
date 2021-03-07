from typing import List
from uuid import uuid4
from loguru import logger
from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.engine.app import neo4j_client
from opulence.engine.controllers import fact as fact_ctrl
from opulence.engine.models.scan import Scan
from opulence.engine.scans.factory import ScanFactory

all_scans = ScanFactory().build()


def create(scan: Scan):
    logger.info(f"Create scan {scan}")
    neo4j_scans.create(neo4j_client, scan)


def add_facts(scan_id: uuid4, facts_ids: List[uuid4]):
    logger.info(f"Add facts {facts_ids} to scan {scan_id}")
    neo4j_scans.add_facts(neo4j_client, scan_id, facts_ids)


def get(scan_id: uuid4):
    logger.info(f"Get scan {scan_id}")
    scan, facts = neo4j_scans.get_user_input_facts(neo4j_client, scan_id)
    scan.facts = fact_ctrl.get_many(facts)
    return scan


def launch(scan: Scan):
    logger.info(f"Launch scan {scan}")
    if scan.scan_type not in all_scans:
        logger.error(f"Scan {scan.scan_type} not found")
        raise ValueError(f"Scan {scan.scan_type} not found")
    all_scans[scan.scan_type]().launch(scan)
