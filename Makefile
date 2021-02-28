

docker:
	docker-compose -f deploy/docker-compose.yml up -d

engine:
	 celery  -A opulence.engine.app worker -B --hostname=engine --loglevel=info
agent:
	 celery  -A opulence.agent.app  worker --hostname=agent --loglevel=info

format:
	tox -e format
