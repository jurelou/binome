import hashlib
import logging
from typing import Optional

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import root_validator, Field

from opulence.common.utils import load_classes_from_module
from time import time
logger = logging.getLogger(__name__)


class BaseFact(BaseModel):
    __hash: Optional[str] = None
    
    
    first_seen: float = Field(default_factory=time)
    last_seen: float = Field(default_factory=time)
    
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

    # @classmethod
    # def elastic_mapping(self, mapping=None):
    #     if map:
    #         map["mappings"]["properties"]["first_seen"] = {"type": "float"}
    #         map["mappings"]["properties"]["last_seen"] = {"type": "float"}
    #         return map
    #     return {"mappings": {"properties": {}}}

    @staticmethod
    def make_mapping(m):
        m["mappings"]["properties"]["first_seen"] = {"type": "float"}
        m["mappings"]["properties"]["last_seen"] = {"type": "float"}
        return m

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping({"mappings": {"properties": {}}})

def load_all_facts():
    facts_modules = load_classes_from_module("opulence/facts", BaseFact)
    facts = {mod.schema()["title"].lower(): mod for mod in facts_modules}
    logger.info(f"Loaded facts: {facts.keys()}")
    return facts


all_facts = load_all_facts()
