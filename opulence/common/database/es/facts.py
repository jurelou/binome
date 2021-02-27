from opulence.common.database.es.base import BaseIndex
from elasticsearch.helpers import bulk

from opulence.common.fact import all_facts
class FactsIndexes(BaseIndex):
  index_name = "facts"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}

  def create_index(self, es_client):
    print(all_facts)
    print("====")
    for fact, body in all_facts.items():
      es_client.indices.create(index=fact, body=body.elastic_mapping(), ignore=400)
      es_client.indices.put_settings(
          index=fact,
          body={"refresh_interval": self.refresh_interval, "number_of_replicas": self.replicas},
      )  
  
  def bulk_upsert(self, es_client, facts):
    def gen_actions(facts):
      for fact in facts:
        yield {
            '_op_type': 'update',
            '_index': self.index_name,
            '_id': fact.hash__,
            'doc': fact.dict(exclude={"hash__"}),
            'doc_as_upsert': True # ????
        }



    print("SALUT", facts[0].firstname)
    return bulk(client=es_client, actions=gen_actions(facts))
