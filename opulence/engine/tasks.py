from opulence.engine.app import celery_app
from opulence.engine.controllers import agents as agents_ctrl
from opulence.engine.controllers import scan as scan_ctrl

@celery_app.task
def reload_agents():
  print("YO")
  agents_ctrl.refresh_agents()


@celery_app.task
def scan():
  print("je scan")
  scan_ctrl.new()


# a = tasks.test_agent.apply_async().get()
# print("@@@@@@@@@@@@@@@@@@@")
# print("res->", a)
# print("@@@@@@@@@@@@@@@@@")




# @celery_app.task(name="engine.scan.launch")
# def scan(scan_type: str, config: BaseFact):
#   print("!!!!!!ENGINE TOTO")


# a = signatures.launch_scan("a-collector", [Person(firstname="a", lastname="b")]).apply_async()
# print("RESYULT", a.get())

# from opulence.engine import remote_tasks
# from opulence.facts.person import Person
# from opulence.common.celery import sync_call
# from opulence.agent import celery_app 

# from opulence.engine import celery_app as tutu


# a = tutu.signature("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])

# a.apply_async()

# a = tutu.send_task("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])
# 
# a.get()

# a = remote_tasks.launch_scan("b-collector", [Person(firstname="lol", lastname="mdr")]).apply_async()
# print("@@@@", a.get())