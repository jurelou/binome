

docker:
	docker-compose -f deploy/docker-compose-engine.yml up -d

engine:
	 celery  -A opulence.engine.app worker -B --hostname=engine --loglevel=info
agent:
	 celery  -A opulence.agent.app  worker --hostname=agent --loglevel=info 
