from config import engine_config

from opulence.facts.person import Person
from opulence.common.celery import create_app
from opulence.common.database.es import create_client, INDEXES
from opulence.common.database.es import fact_index

es_client = create_client(engine_config.elasticsearch)
app = create_app()
app.conf.update(engine_config.celery)

#from celery.execute import send_task    
#send_task('toto:tasque')

# p = Person(firstname="fname", lastname="lname")
# print("ADD", p)
# r = fact_index.bulk_upsert(es_client, [p])
# print("RES=>", r)

# p = Person(firstname="fname", lastname="lname", age=1222222222222)
# print("ADD", p)
# r = fact_index.bulk_upsert(es_client, [p])
# print("RES=>", r)



# print("====")
# for a in p:
#     print(a)



#def scan_signature(collector_name):    
#    return app.signature(f"{collector_name}:tasque", immutable=True)

#scan_signature("toto").delay()



import docker

client = docker.from_env()


a = client.containers.run("alpine", command=["ls", "-lah"])
print(a)

