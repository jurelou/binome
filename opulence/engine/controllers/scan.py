from opulence.common.database.neo4j import scans as neo4j_scans

from opulence.engine.app import neo4j_client

from opulence.engine.models.scan import Scan


def create(scan: Scan):
    neo4j_scans.create(neo4j_client, scan)
