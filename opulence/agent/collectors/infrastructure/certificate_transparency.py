from opulence.agent.collectors.base import BaseCollector
from opulence.facts.domain import Domain
import httpx
class CertificateTransparency(BaseCollector):
    config = {
        "name": "Certificate transparency",
    }

    def callbacks(self):
        return {Domain: self.from_domain}

    def from_domain(self, domain):
        res = httpx.get(f"https://crt.sh/?q=%.{domain.fqdn}&output=json", timeout=30)
        if res:
            for entry in res.json():
                yield Domain(fqdn=entry["common_name"], certificate_issuer=entry["issuer_name"])
        else:
            print(f"CT Error: {res}")