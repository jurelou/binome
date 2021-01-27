from opulence.agent.collectors.base import BaseCollector, BaseConfig
import docker
from typing import Union, List
#class DockerConfig(BaseConfig):
#    docker_image: str


class DockerCollector(BaseCollector):

    def configure(self):
        self.config = BaseConfig(**self.config)
        self.__client = docker.from_env()

    def __pull_image(self, image,  tag=None, all_tags=False, **kwargs):
        return self.__client.images.pull(image, tag=tag, all_tags=all_tags, **kwargs)

    def run_container(self, image, command: Union[str, List[str]], **kwargs):
        # https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run
        # self.__pull_image(image) ??
        return self.__client.containers.run(image, command, auto_remove=True, detach=False, network_mode="bridge", remove=True, **kwargs)
