from pydantic import BaseConfig
from pydantic import BaseModel


class BaseFact(BaseModel):
    __hash: Optional[str] = None

    @root_validator
    def set_hash(cls, values):
        values.pop("__hash", None)
        m = hashlib.sha256()
        for k in sorted(values):
            m.update(str(k).encode() + str(values[k]).encode())
        values["__hash"] = m.hexdigest()
        return values
 
    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
