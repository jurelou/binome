from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.person import Person
from opulence.facts.domain import Domain
import re

class Gobuster(DockerCollector):
    config = {
        "name": "gobuster",
        "docker": {
            "build_context": get_actual_dir(),
        },
    }

    def callbacks(self):
        return {Domain: self.from_domain}


    def from_domain(self, domain):
        yield from self.run_hacker_target(domain.fqdn)
        # hello = self.run_container(command="whoami")
        # print("exec docker collector")
        # yield Person(firstname="dummy docker collector", lastname=hello)
        # yield Email(address="yes")