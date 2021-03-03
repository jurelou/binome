from typing import Optional
from opulence.engine.models.scan import Scan

class   BaseScan:
    name: Optional[str] = None

    def __init__(self, config=None):
        if not self.name:
            raise ValueError(f"{type(self).__name__} should contain a `name` property")

    def launch(self, scan: Scan):
        print("LAUNCH")