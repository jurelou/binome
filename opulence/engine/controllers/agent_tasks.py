from opulence.common.celery import async_call
from opulence.engine.app import celery_app

def scan():
    print("launch scan")
    task = async_call(
        celery_app,
        "scan",
        queue="agent_scan",
        routing_key="scansomekey"
    )
    return task