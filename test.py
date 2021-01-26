from config import engine_config

from opulence.facts.person import Person
from opulence.celery import configure_celery
from opulence.common.database.es import create_client, INDEXES
from opulence.common.database.es import fact_index

es_client = create_client(engine_config.elasticsearch)
app = configure_celery(engine_config.celery_broker)


#from celery.execute import send_task    
#send_task('toto:tasque')

p = Person(firstname="fname", lastname="lname")
print("ADD", p)
r = fact_index.bulk_upsert(es_client, [p])
print("RES=>", r)

p = Person(firstname="fname", lastname="lname", age=32)
print("ADD", p)
r = fact_index.bulk_upsert(es_client, [p])
print("RES=>", r)



#def scan_signature(collector_name):    
#    return app.signature(f"{collector_name}:tasque", immutable=True)

#scan_signature("toto").delay()

