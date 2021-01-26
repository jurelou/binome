from opulence.common.database.es.base import BaseIndex
from elasticsearch.helpers import bulk

class FactIndex(BaseIndex):
  index_name = "facts"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}
  
  
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
        print("GGOOGOGOGOG")
    print("SALUT", facts[0].firstname)
    return bulk(client=es_client, actions=gen_actions(facts))
