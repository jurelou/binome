from opulence.common.database.es.base import BaseIndex
from elasticsearch.helpers import bulk

class FactIndex(BaseIndex):
  index_name = "facts"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}

  # def create_index(self, es_client):
  #     es_client.indices.create(index=self.index_name, body=self.mapping)
  #     es_client.indices.put_settings(
  #         index=self.index_name,
  #         body={"refresh_interval": self.refresh_interval, "number_of_replicas": self.replicas},
  #     )  
  
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
