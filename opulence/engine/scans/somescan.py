from opulence.engine.scans.base import BaseScan
from opulence.engine.models.scan import Scan

from opulence.engine.controllers import agent_tasks

class   somescan(BaseScan):
    name = "simplescan"
    
    def launch(self, scan: Scan):
        print("LAUNCHSCANLOL", scan)
        agent_tasks.scan("dummy-docker-collector", scan.facts)
