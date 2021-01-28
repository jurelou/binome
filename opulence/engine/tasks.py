from opulence.engine import celery_app
# from opulence.agent.scan import tasks
# from opulence.agent.scan import signatures
from opulence.facts.person import Person
from opulence.common.fact import BaseFact


# a = tasks.test_agent.apply_async().get()
# print("@@@@@@@@@@@@@@@@@@@")
# print("res->", a)
# print("@@@@@@@@@@@@@@@@@")

@celery_app.task(name="engine.scan.launch")
def scan(scan_type: str, config: BaseFact):
  print("!!!!!!ENGINE TOTO")


# a = signatures.launch_scan("a-collector", [Person(firstname="a", lastname="b")]).apply_async()
# print("RESYULT", a.get())

# from opulence.engine import remote_tasks
# from opulence.facts.person import Person
# a = remote_tasks.launch_scan("b-collector", [Person(firstname="lol", lastname="mdr")]).delay()
# print("!!!!!!!!!!!", a.get())
