from opulence.agent import tasks
from opulence.common.base_fact import BaseFact
from typing import List

def launch_scan(collector_name: str, facts: List[BaseFact]):
    return tasks.launch_scan.signature(args=[collector_name, facts])
