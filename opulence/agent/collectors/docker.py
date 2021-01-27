from opulence.agent.collectors.base import BaseCollector, BaseConfig

class DockerConfig(BaseConfig):
    docker_image: str


class DockerCollector(BaseCollector):

    def configure(self):
        self.config = DockerConfig(**self.config)
