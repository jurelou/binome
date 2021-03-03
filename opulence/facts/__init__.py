from opulence.common.utils import load_classes_from_module
from opulence.common.fact import BaseFact
def load_all_facts():
    facts = {mod.schema()["title"]: mod for mod in load_classes_from_module("opulence/facts", BaseFact)}
    print(f"Loaded facts: {facts}")
    return facts

all_facts = load_all_facts()
