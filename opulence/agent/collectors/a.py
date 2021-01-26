from opulence.common.collector import BaseCollector
from opulence.facts.person import Person
from opulence.facts.email import Email

class a(BaseCollector):
    config = {
        "name": "a-collector",
    }

    def callbacks(self):
        return {
            Person: self.cb,
            Email: self.cb,
        }
    
    def cb(self, ok):
        yield Person(firstname="lol", lastname="mdr")
