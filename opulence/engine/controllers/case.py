from opulence.engine.controllers import agent_tasks
from opulence.common.database.neo4j import cases as neo4j_cases
from opulence.common.database.neo4j import scans as neo4j_scans

from opulence.engine.app import neo4j_client

from opulence.engine.models.case import Case
from opulence.engine.models.scan import Scan

from uuid import uuid4

# def create: crée dans neo3j
def create(case: Case):
    print("new case")
    case.bite = "mdr"
    neo4j_cases.create(neo4j_client, case)

    print(f"Created case  {case}")

def add_scan(case_id: uuid4, scan_id: uuid4):
    neo4j_cases.add_scan(neo4j_client, case_id=case_id, scan_id=scan_id)

# from opulence.engine.controllers import agent_tasks
# from opulence.common.database.neo4j import scans as neo4j_scans
# from opulence.engine.app import neo4j_client

# from opulence.engine.models.scan import Scan

# # def create: crée dans neo3j
# def new():
#     print("new scan")
#     from opulence.facts.person import Person
#     scan = Scan()

#     agent_tasks.scan(
#         "dummy-docker-collector", [Person(firstname="flol", lastname="lmdr")]
#     )

#     scan.bite = "mdr"
#     neo4j_scans.create_scan(neo4j_client, scan.external_id.hex, scan.dict(exclude={"external_id"}))