from opulence.engine.models.scan import Scan
from uuid import uuid4
from typing import List

def create(client, scan: Scan):
        with client.session() as session:
            session.run(
                "CREATE (scan:Scan {external_id: $external_id}) "
                "SET scan += $data",
                external_id=scan.external_id.hex,
                data=scan.dict(exclude={"external_id", "facts"}),
            )

def add_facts(client, scan_id: uuid4, facts_ids: List[str]):
        formated_links = [{"from": scan_id.hex, "to": fact} for fact in facts_ids]

        with client.session() as session:
            session.run(
                "UNWIND $links as link "
                "MATCH (from:Scan), (to:Fact) "
                "WHERE from.external_id = link.from AND to.external_id = link.to "
                "CREATE (from)-[r:MDRRR]->(to)",
                links=formated_links
            )
