from neo4j import GraphDatabase


def create_client(config):
    print(f"Create neo4j client: {config}")
    return GraphDatabase.driver(config.endpoint, auth=(config.username, config.password))

def create_constraints(client):
    with client.session() as session:
        session.run("CREATE CONSTRAINT case_unique_id IF NOT EXISTS ON (c:Case) ASSERT c.external_id IS UNIQUE")
        session.run("CREATE CONSTRAINT scan_unique_id IF NOT EXISTS ON (s:Scan) ASSERT s.external_id IS UNIQUE")


def flush(client):
    print("=======================flush")
    with client.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    print("FLUSH")