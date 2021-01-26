from config import agent_config
from opulence.agent import celery_app
from opulence.common.fact import BaseFact
from typing import List
from opulence.common import exceptions
# from celery import states
# from celery.exceptions import Ignore

from opulence.agent import COLLECTORS

@celery_app.task(name="scan.test")
def test_agent():
    return "salut"
    # for i in [1, 2, 3, 4]:
    #     yield i

@celery_app.task(throws=(exceptions.BaseAgentException), name="scan.launch", acks_late=True)
def launch_scan(collector_name: str, facts: List[BaseFact]):

    print(COLLECTORS)
    if collector_name not in COLLECTORS:
        raise exceptions.CollectorNotFound(f"Collector {collector_name} not found.")

    if not COLLECTORS[collector_name]["active"]:
        raise exceptions.CollectorDisabled(f"Collector {collector_name} is not enabled.")

    try:
        COLLECTORS[collector_name]["instance"].collect(facts)
    except exceptions.CollectorRuntimeError as err:
        print("->", err)


    print(collector_name in COLLECTORS)
    print("!!!!!!JESCAcool", collector_name)
    print("=====", facts)
    print("--", COLLECTORS)
