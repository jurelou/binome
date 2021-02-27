from opulence.engine.controllers import agent_tasks

def new():
    print("new scan")
    agent_tasks.scan()