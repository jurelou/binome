from opulence.facts.factory import FactFactory

def load_all_facts():
    facts = {
        mod.schema()["title"]: mod
        for mod in load_classes_from_module("opulence/facts", BaseFact)
    }
    print(f"Loaded facts: {facts}")
    return facts


all_facts = FactFactory().build()
print(f"ALL facts: {all_facts}")