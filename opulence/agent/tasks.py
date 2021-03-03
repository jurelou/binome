from typing import List

from celery import current_task
from celery.utils.log import get_task_logger

from opulence.agent.app import celery_app
from opulence.agent.app import es_client
from opulence.agent import exceptions
from opulence.common.database.es import facts as facts_index
from opulence.common.fact import BaseFact
from opulence.agent.collectors.factory import CollectorFactory

logger = get_task_logger(__name__)

all_collectors = CollectorFactory().items



@celery_app.task(name="scan", throws=(exceptions.BaseAgentException))
def scan(facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info["routing_key"]

    print("====", all_collectors)
    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(f"Collector {collector_name} not found.")
    if not all_collectors[collector_name]["active"]:
        raise exceptions.CollectorDisabled(
            f"Collector {collector_name} is not enabled.",
        )

    collect_result = all_collectors[collector_name]["instance"].collect(facts)
    print("FOUND RES", collect_result)
    facts_index.bulk_upsert(es_client, collect_result.facts)
    result = collect_result.dict(exclude={"facts"})
    result["facts"] = [fact.hash__ for fact in collect_result.facts]

    return result


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
