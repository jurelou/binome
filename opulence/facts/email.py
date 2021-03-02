from opulence.common.fact import BaseFact


class Email(BaseFact):
    address: str


    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping({
            "mappings": {
                "properties": {
                    "lastname": {"type": "keyword"},
                    "firstname": {"type": "keyword"},
                },
            }
        })
