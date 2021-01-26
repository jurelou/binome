from pydantic import BaseConfig
from pydantic import BaseModel


class BaseFact(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
