from config import agent_config
from opulence.agent import celery_app
from opulence.common.fact import BaseFact
from typing import List
from opulence.agent import exceptions
# from celery import states
# from celery.exceptions import Ignore

from opulence.agent.collectors import all_collectors

@celery_app.task(name="scan.test")
def test_agent():
    return "salut"
    # for i in [1, 2, 3, 4]:
    #     yield i

#@celery_app.task(throws=(exceptions.BaseAgentException), name="scan.launch", acks_late=True)
@celery_app.task(throws=(exceptions.BaseAgentException), name="scan.launch")
def launch_scan(collector_name: str, facts: List[BaseFact]):

    print(all_collectors)
    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(f"Collector {collector_name} not found.")

    if not all_collectors[collector_name]["active"]:
        raise exceptions.CollectorDisabled(f"Collector {collector_name} is not enabled.")

    
    result = all_collectors[collector_name]["instance"].collect(facts)
    result = result.dict()
    return result
