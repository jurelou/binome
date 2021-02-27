from opulence.common.fact import BaseFact
from typing import List
from opulence.agent import exceptions
from opulence.agent.app import celery_app, es_client
from opulence.agent.controllers.collectors import all_collectors

# from opulence.common.database.es import fact_index 
from celery import current_task

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@celery_app.task(name="scan", throws=(exceptions.BaseAgentException))
def scan(facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info['routing_key']

    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(f"Collector {collector_name} not found.")
    if not all_collectors[collector_name]["active"]:
        raise exceptions.CollectorDisabled(f"Collector {collector_name} is not enabled.")


    collect_result = all_collectors[collector_name]["instance"].collect(facts)
    # upserted_facts = fact_index.bulk_upsert(es_client, collect_result.facts)


    # result = collect_result.dict(exclude={"facts"})
    # result["facts"] = upserted_facts
    
    # return result

    return {"salut": "collect_result"}


# @celery_app.task(throws=(exceptions.BaseAgentException), name="agent.scan.launch")
# def launch_scan(collector_name: str, facts: List[BaseFact]):
#     print("AAAAAAAAAAAAAAA")
#     print(f"launch scan {collector_name}")

#     if collector_name not in all_collectors:
#         raise exceptions.CollectorNotFound(f"Collector {collector_name} not found.")

#     if not all_collectors[collector_name]["active"]:
#         raise exceptions.CollectorDisabled(f"Collector {collector_name} is not enabled.")

    
#     collect_result = all_collectors[collector_name]["instance"].collect(facts)

#     upserted_facts = fact_index.bulk_upsert(es_client, collect_result.facts)


#     result = collect_result.dict(exclude={"facts"})
#     result["facts"] = upserted_facts
    
#     return result
