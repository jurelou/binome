from opulence.agent.collectors.base import BaseCollector
from opulence.facts.email import Email
from opulence.facts.person import Person


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
