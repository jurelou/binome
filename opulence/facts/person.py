from opulence.common.fact import BaseFact


class Person(BaseFact):
    lastname: str
    firstname: str

    def elastic_mapping():
        return {
            "mappings": {
                "properties": {
                    "lastname": {
                        "type": "keyword"
                    },
                    "firstname": {
                        "type": "keyword"
                    }

                }
            }
        }