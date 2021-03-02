# TODO:

- proper logging

- central docker registry: https://docs.docker.com/registry/deploying/

- docker: build & push  & pull dans le registry
    dans le collecteur: prerequis
# noms:

*inoma


binome

thoth

ocaro

ocai


relations = [{'from': 'man', 'to': 'woman', 'properties': {'cost': 0}},
{'from': 'woman', 'to': 'baby', 'properties': {'cost': 0}]


 query = """
    UNWIND {{relations}} as row
    MATCH (from:SINGLE_NODE {{name:row.from}})
    MATCH (to:SINGLE_NODE {{name:row.to}})
    MERGE (from)-[rel:IS_CONNECTED]->(to)
    ON CREATE SET rel += row.properties
    """.format(relations=relations)

    session.run(query, relations=relations)


session.run(query, relations=relations)
