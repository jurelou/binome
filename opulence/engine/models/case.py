from pydantic import BaseModel, Field, BaseConfig
import uuid
from time import time


class Case(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }