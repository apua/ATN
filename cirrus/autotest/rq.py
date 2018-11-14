"""
RQ utils.
"""
import time
import uuid

from redis import Redis
from rq import decorators
from rq.job import Job
from django.conf import settings


def task(func):
    """
    A wrapper of `rq.decorators.job` for simply use.

    .. code:: Python

        @task
        def f(*a, **kw):
            pass
        job = f.delay()
    """
    queuename = settings.AUTOTEST_QUEUENAME
    connection = Redis()
    return decorators.job(queuename, connection=connection)(func)


def wait_for_finished(rq_jid: str, timeout):
    job = Job.fetch(rq_jid, connection=Redis())
    for _ in range(timeout):
        time.sleep(1)
        if job.status == 'finished':
            return
    raise Exception('{job.status} is not finished after {timeout} seconds'.format(**locals()))
