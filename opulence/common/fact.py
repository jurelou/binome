from pydantic import BaseConfig
from pydantic import BaseModel, root_validator
from typing import Optional
import hashlib

class BaseFact(BaseModel):
    __hash: Optional[str] = None

    def __iter__(self):
        raise TypeError

    @root_validator
    def set_hash(cls, values):
        values.pop("hash__", None)
        m = hashlib.sha256()
        required_fields = cls.schema()["required"]
        for k in sorted(values):
            if k in required_fields:
                m.update(str(k).encode() + str(values[k]).encode())
        values["hash__"] = m.hexdigest()
        return values
 
    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
