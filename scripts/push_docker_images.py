#!/usr/bin/env python3
import docker

from pathlib import Path
from docker import APIClient

docker_client = APIClient()
docker_registry_endpoint = "localhost:5000"


def get_dockerfiles():
  return [ (path.parent, path.name) for path in Path('./deploy/docker_images').rglob('*.dockerfile') ]

def build_dockerfile(path, filename):
  tag = "localhost:5000/opulence/nmap:latest"
  stream  = docker_client.build(path="./deploy/docker_images", dockerfile=filename, tag=tag, rm=True, decode=True)
  for chunk in stream:
      if 'stream' in chunk:
          for line in chunk['stream'].splitlines():
              print(line)
  return tag

def push_docker_image(image_name):
  stream = docker_client.push(repository=image_name, stream=True, decode=True)
  for chunk in stream:
      if 'stream' in chunk:
          for line in chunk['stream'].splitlines():
              print(line)
  print("ok")

def pull_docker_image(image_name):
  stream = docker_client.pull(repository=image_name, stream=True, decode=True)
  for chunk in stream:
      if 'stream' in chunk:
          for line in chunk['stream'].splitlines():
              print(line)

def list_images():
  for image in docker_client.images():
    print(f"-> {image}")


for path, filename in get_dockerfiles():
  print(f"Found dockerfile {path} / {filename}")
  image = build_dockerfile(path, filename)
  push_docker_image(image)
# list_images()
