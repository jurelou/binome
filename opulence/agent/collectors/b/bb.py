from opulence.common.collector import BaseCollector
from opulence.facts.person import Person
from opulence.facts.email import Email

class b(BaseCollector):
    config = {
        "name": "b-collector",
    }

    def callbacks(self):
        return {
            Person: self.cb,
            Email: self.cb,
        }
    
    def cb(self, person):
        return Person(firstname="this", lastname="person")

