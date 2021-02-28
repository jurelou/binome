from typing import List

from celery.result import allow_join_result

from opulence.common.celery import async_call
from opulence.common.fact import BaseFact
from opulence.engine.app import celery_app


@celery_app.task(ignore_result=True, acks_late=True)
def scan_success(result, collector_name, facts):
    print("SUCCESS", result)


@celery_app.task
def scan_error(task_id, collector_name):
    print("ERRORRRRRR")
    # with allow_join_result():
    #     print("ERROR", task_id, collector_name)
    # result = celery_app.AsyncResult(task_id)
    # print("result ->", result.state)
    # print("result ->", result.get())

    # try:
    #     log.info("file:%s probe %s", file, probe)
    #     with session_query() as session:
    #         result = probe_ctrl.create_error_results(probe, "job error",
    #                                                  session)
    #         celery_frontend.scan_result(file, probe, result)
    # except Exception as e:
    #     log.exception(type(e).__name__ + " : " + str(e))
    #     raise job_error.retry(countdown=5, max_retries=3, exc=e)


def scan(collector_name: str, facts: List[BaseFact]):
    print("launch scan")

    task = async_call(
        celery_app,
        "scan",
        link=scan_success.signature([collector_name, facts]),
        link_error=scan_error.signature([collector_name]),
        queue=collector_name,
        args=[facts],
    )
    return task
