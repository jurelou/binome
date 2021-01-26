from opulence.agent import celery_app 
from opulence.common.base_fact import BaseFact
from typing import List

def launch_scan(collector_name: str, facts: List[BaseFact]):
    return celery_app.signature("scan.launch", immutable=True)
    return tasks.launch_scan.signature(args=[collector_name, facts])
