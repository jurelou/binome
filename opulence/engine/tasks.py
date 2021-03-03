from uuid import uuid4

from opulence.engine.app import celery_app
from opulence.engine.controllers import agents as agents_ctrl
from opulence.engine.controllers import case as case_ctrl
from opulence.engine.controllers import fact as fact_ctrl
from opulence.engine.controllers import scan as scan_ctrl
from opulence.engine.models.case import Case
from opulence.engine.models.scan import Scan


@celery_app.task
def reload_agents():
    print("YO")
    agents_ctrl.refresh_agents()


@celery_app.task
def add_case(case: Case):
    print("new case")
    case_ctrl.create(case)


@celery_app.task
def add_scan(case_id: uuid4, scan: Scan):
    print("new scan")

    scan_ctrl.create(scan)
    case_ctrl.add_scan(case_id, scan.external_id)

    fact_ctrl.add_many(scan.facts)
    facts_ids = [fact.hash__ for fact in scan.facts]

    scan_ctrl.add_facts(scan.external_id, facts_ids)


@celery_app.task
def launch_scan(scan_id: uuid4):
    print(f"launch scan {scan_id}")
    scan = scan_ctrl.get(scan_id)
    scan_ctrl.launch(scan)
    # scan_ctrl.create(scan)
    # case_ctrl.add_scan(case_id, scan.external_id)


# a = tasks.test_agent.apply_async().get()
# print("@@@@@@@@@@@@@@@@@@@")
# print("res->", a)
# print("@@@@@@@@@@@@@@@@@")


# @celery_app.task(name="engine.scan.launch")
# def scan(scan_type: str, config: BaseFact):
#   print("!!!!!!ENGINE TOTO")


# from opulence.engine import remote_tasks
# from opulence.facts.person import Person
# from opulence.common.celery import sync_call
# from opulence.agent import celery_app



# a = tutu.signature("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])

# a.apply_async()

# a = tutu.send_task("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])
#
# a.get()

# a = remote_tasks.launch_scan("b-collector", [Person(firstname="lol", lastname="mdr")]).apply_async()
# print("@@@@", a.get())
