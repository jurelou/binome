#!/usr/bin/env python3
import docker

from pathlib import Path

docker_client = docker.from_env()
docker_registry_endpoint = "localhost:5000"


def get_dockerfiles():
  #retourner un tuple path; filename
  return [ path.name for path in Path('./deploy/docker_images').rglob('*.dockerfile') ]

def build_dockerfile(path, filename):
  image, _ = docker_client.images.build(path=path, dockerfile=filename, tag="latest", rm=True)
  return image
  
def push_docker_image(image_name):
  image, _ = docker_client.images.push(repository=docker_registry_endpoint, dockerfile=filename, tag="latest", rm=True)
  return image

def pull_docker_image():
  pass

def list_images():
  for image in docker_client.images.list():
    print(f"-> {image}")


for path, filename in get_dockerfiles():
  print(f"Found dockerfile {dockerfile}")
  image = build_dockerfile(path, filename)
  
list_images()
