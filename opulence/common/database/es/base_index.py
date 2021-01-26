
class BaseIndex():
  index_name = None
  replicas = 0
  refresh_interval = "30s"

  @property
  def mapping(self):
    return {"mappings": {"properties": {}}}

 
  def create_index(self, es_client):
      es_client.indices.create(index=self.index_name, body=self.mapping)
      es_client.indices.put_settings(
          index=self.index_name,
          body={"refresh_interval": self.refresh_interval, "number_of_replicas": self.replicas},
      )

  def remove_index(self, es_client):
      es_client.indices.delete(index=self.index_name)

