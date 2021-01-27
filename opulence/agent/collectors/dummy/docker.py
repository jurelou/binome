from opulence.agent.collectors.base import BaseCollector, BaseConfig
import docker
from typing import Union, List
#class DockerConfig(BaseConfig):
#    docker_image: str


class DockerCollector(BaseCollector):
