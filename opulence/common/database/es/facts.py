from opulence.common.database.es.base import BaseIndex
from elasticsearch.helpers import parallel_bulk

class FactIndex(BaseIndex):
  index_name = "facts"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}
  
  
  def bulk_upsert(self, es_client, actions):
    actions = [{'username':'Tom', "id": 1}]
    
    def gen_actions(actions):
      for action in actions:
        _id = action.pop("id")
        yield {
            '_op_type': 'update',
            '_index': self.index_name,
            '_id': _id,
            'doc': action,
            "doc_as_upsert":True # ????
        }
    es.parallel_bulk(client=es_client, actions=gen_actions(actions))
