# from celery import Celery
# from kombu.serialization import register
# import logging
# import os
# from celery.signals import after_setup_logger


# class TaskRouter(object):
#     def route_for_task(self, task, *args, **kwargs):
#         if ":" not in task:
#             return {"queue": "default"}
#         namespace, _ = task.split(":")
#         return {"queue": namespace}

# @after_setup_logger.connect
# def setup_loggers(logger, *args, **kwargs):
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh = logging.FileHandler('opulence.log')
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)


# def configure_celery(config, **kwargs):
#     app = Celery(__name__, **kwargs)
#     config.update(
#         {
#             "task_routes": {
#                     'feeds.tasks.import_feed': {
#                         'queue': 'feed_tasks',
#                         'routing_key': 'feed.import',
#                     },
#             },
#             # "accept_content": ["customEncoder", "application/json"],
#             # "task_serializer": "customEncoder",
#             # "result_serializer": "customEncoder",
#         }
#     )
#     app.conf.task_default_exchange_type = 'topic'
#     app.conf.update(config)
#     # if custom_encoder:
#     #     register(
#     #         "customEncoder",
#     #         jsonEncoder.custom_dumps,
#     #         jsonEncoder.custom_loads,
#     #         content_type="application/x-customEncoder",
#     #         content_encoding="utf-8",
#     #     )
#     return app