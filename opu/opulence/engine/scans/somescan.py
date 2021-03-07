from opulence.engine.controllers import agent_tasks
from opulence.engine.models.scan import Scan
from opulence.engine.scans.base import BaseScan


class somescan(BaseScan):
    name = "simplescan"

    def launch(self, scan: Scan):
        print("LAUNCHSCANLOL", scan)
        agent_tasks.scan("dummy-docker-collector", scan.facts)
