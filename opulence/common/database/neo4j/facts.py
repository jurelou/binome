from opulence.engine.models.scan import Scan
from uuid import uuid4


def create_many(client, scan: Scan):
        with client.session() as session:
            session.run(
                "CREATE (scan:Scan {external_id: $external_id}) ",
                # "SET scan += $data",
                external_id=scan.external_id.hex,
                # data=scan.dict(exclude={"external_id"}),
            )
