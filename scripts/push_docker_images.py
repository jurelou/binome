#!/usr/bin/env python3
import docker

from pathlib import Path

def get_dockerfiles():  
  return [ path.name for path in Path('./deploy/docker_images').rglob('*.dockerfile') ]

