from opulence.agent import celery_app 
from opulence.common.fact import BaseFact
from typing import List
from opulence.agent import tasks


def launch_scan(collector_name: str, facts: List[BaseFact]):
    return celery_app.signature("scan.launch", args=[collector_name, facts])
