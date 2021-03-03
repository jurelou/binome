from opulence.common.factory import Factory
from opulence.common.fact import BaseFact


class FactFactory(Factory):

    def build(self):
        facts = {
            mod.schema()["title"]: mod
            for mod in self.load_classes_from_module("opulence/facts", BaseFact)
        }
        self.items = facts
        return facts
        

