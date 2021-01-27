from opulence.agent.collectors.docker import DockerCollector

from opulence.facts.person import Person

class DummyDocker(DockerCollector):
    config = {
        "name": "dummy-docker-collector",
    }

    def callbacks(self):
        return { Person: self.cb }

    def cb(self, person):
      hello = self.run_container("ubuntu", command=['echo', '"hi"'])
      yield Person(firstname="dummy docker collector", lastname=hello)
