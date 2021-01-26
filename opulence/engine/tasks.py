from opulence.engine import celery_app
# from opulence.agent.scan import tasks
# from opulence.agent.scan import signatures
from opulence.facts.person import Person
from opulence.common.fact import BaseFact


# a = tasks.test_agent.apply_async().get()
# print("@@@@@@@@@@@@@@@@@@@")
# print("res->", a)
# print("@@@@@@@@@@@@@@@@@")

# @celery_app.task(name="engine.toto")
# def single_collector_scan(collector_name: str, facts: List[BaseFact]):
#     print("!!!!!!ENGINE TOTO")


# a = signatures.launch_scan("a-collector", [Person(firstname="a", lastname="b")]).apply_async()
# print("RESYULT", a.get())
