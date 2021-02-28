def create_scan(client, id, data):
        with client.session() as session:
            session.run(
                "MERGE (s:Scan {external_id: $external_id}) " "SET s += $data",
                external_id=id,
                data=data,
            )