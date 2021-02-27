import json

from opulence.common.fact import BaseFact, all_facts


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseFact):
            return {"__type__": "__fact__", "fact": obj.json(), "fact_type": type(obj).__name__.lower()}
        return json.JSONEncoder.default(self, obj)

def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__fact__":
            return all_facts[obj["fact_type"]].parse_raw(obj["fact"])
    return obj

def json_dumps(obj):
    return json.dumps(obj, cls=encode)

def json_loads(obj):
    return json.loads(obj, object_hook=decode)
