from neo4j import GraphDatabase


def create_client(config):
    print(f"Create neo4j client: {config}")
    return GraphDatabase.driver(config.endpoint, auth=(config.username, config.password))

def create_constraints():
    pass