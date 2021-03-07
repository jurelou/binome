# import celery
from redbeat import RedBeatSchedulerEntry
from redbeat.schedulers import get_redis
from loguru import logger
# from opulence.config import engine_config

# def configure_tasks():
#     interval = celery.schedules.schedule(run_every=engine_config.refresh_agents_interval)
#     entry = RedBeatSchedulerEntry("reload_agents", 'opulence.engine.tasks.reload_agents', interval, app=celery_app)
#     entry.save()

def flush():
    logger.info("Flush periodic tasks")
    redis = get_redis()
    for key in redis.scan_iter("redbeat:*"):
        if key not in ("redbeat::lock"):
            redis.delete(key)

def add_periodic_task(app, interval, task_path):
    print(f"Create task {task_path}")
    entry = RedBeatSchedulerEntry("too", task_path, interval, app=app)
    entry.save()
