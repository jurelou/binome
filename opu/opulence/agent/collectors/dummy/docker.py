from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.person import Person


class DummyDocker(DockerCollector):
    config = {
        "name": "dummy-docker-collector",
        "docker": {
            # "image": "ubuntu:latest"
            "build_context": get_actual_dir(),
        },
    }

    def callbacks(self):
        return {Person: self.cb}

    def cb(self, person):
        hello = self.run_container(command="--help")
        print("exec docker collector")
        yield Person(firstname="dummy docker collector", lastname=hello)
