from opulence.engine.controllers import agent_tasks

def new():
    print("new scan")
    from opulence.facts.person import Person
    agent_tasks.scan("b-collector", [Person(firstname="flol", lastname="lmdr")])
