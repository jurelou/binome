from opulence.engine.controllers import agent_tasks
from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.engine.app import neo4j_client

from opulence.engine.models.scan import Scan

# def create: crée dans neo3j
def new():
    print("new scan")
    from opulence.facts.person import Person
    scan = Scan()

    agent_tasks.scan(
        "dummy-docker-collector", [Person(firstname="flol", lastname="lmdr")]
    )

    scan.bite = "mdr"
    neo4j_scans.create_scan(neo4j_client, scan.external_id.hex, scan.dict(exclude={"external_id"}))