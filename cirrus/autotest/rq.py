"""
RQ utils
"""

from redis import Redis
from rq.decorators import job

from .apps import AutotestConfig as Config


def task(func):
    """
    A wrapper of `rq.decorators.job` for simply use.

    .. code:: Python

        @task
        def f(*a, **kw):
            pass
        job = f.delay()
    """
    queue_name = Config.name
    connection = Redis()
    return job(queue_name, connection=connection)(func)
