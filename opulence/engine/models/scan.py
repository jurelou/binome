from pydantic import BaseModel, Field, BaseConfig
import uuid
from opulence.common.fact import BaseFact
from typing import List

class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    facts: List[BaseFact]
    collector_name: str

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }
