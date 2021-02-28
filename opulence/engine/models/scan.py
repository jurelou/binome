from pydantic import BaseModel, Field, BaseConfig
import uuid



class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
