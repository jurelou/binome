from config import engine_config

from opulence.celery import configure_celery

app = configure_celery(engine_config.celery_broker)


from celery.execute import send_task    
send_task('toto:tasque')


def scan_signature(collector_name):    
    return app.signature(f"{collector_name}:tasque", immutable=True)

scan_signature("toto").delay()