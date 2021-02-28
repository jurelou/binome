from opulence.config import engine_config
from opulence.engine.app import celery_app

available_agents = {}


def refresh_agents():
    global available_agents

    def _get_agents():
        workers = celery_app.control.inspect().active_queues() or {}
        for name, queues in workers.items():
            if any(q["name"] == "agent_scan" for q in queues):
                conf = celery_app.control.inspect([name]).conf()
                yield name, conf[name]["collectors"]

    print("go")
    available_agents = {agent: config for agent, config in _get_agents()}
    print(f"Available agents: {available_agents.keys()}")
