from opulence.agent.collectors.base import BaseCollector, BaseConfig

class DockerConfig(BaseConfig):
    image: str


class DockerCollector(BaseCollector):

    def configure(self):
        self.config = DockerConfig(**self.config)
