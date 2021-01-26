from opulence.common.database.es.base_index import BaseIndex


class FactIndex(BaseIndex):
  index_name = "facts"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}
