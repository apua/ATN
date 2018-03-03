"""
This module implements method to "submit" and "stop" test execution.

Current test execution steps:

1.  Create a workspace
2.  Generate test data and put them into workspace
3.  Execute test with `pybot` (may be stopped during execution)
4.  Collect test report is existing
"""


from .models import TestExecution, Pybot


def stop_test_execution(te: TestExecution) -> TestExecution:
    import os, signal

    stop_pybot = lambda pid: os.kill(pid, signal.SIGINT)
    stop_pybot(te.pid)
    wait_until_killed(te.pid)  # to be implemented
    assert test_report_exist()  # to be implemented
    collect_test_report(to=te.report)  # to be implemented

    return te


def submit_test_execution(test_data_source: dict) -> TestExecution:
    generate_test_data(test_data_source)  # to be implemented
    te = TestExecution()
    te.save()  # write to database for later updating
    rq_job = execute_test.delay(te_id=te.id)
    te.task_id = rq_job.id  # update RQ job id
    te.save()
    return te


def task(func):
    r"""
    A wrapper of `rq.decorators.job` for simply use.

    .. code:: Python

        @task
        def f(*a, **kw):
            pass
        job = f.delay()
    """
    from redis import Redis
    from rq.decorators import job

    from .apps import AutomatedTestConfig as Config

    # NOTE: the 1st parameter of `rq.decorators.job` is *queue name*
    #       rather than queue object in fact
    queue_name = f'{Config.name}'
    connection = Redis()
    # NOTE: may not change RQ's default arguments as below
    #
    # -   `timeout`
    #         :default: None
    #
    #         The max job run time, it will kill `pybot` directly.
    #         Bad for generating test report.
    #
    # -   `ttl`
    #         :default: None
    #
    #         The max job *queue* time.
    #
    # - `result_ttl`
    #         :default: 500
    #
    #         The expiration of stored job result.
    #         Unimportent obviously.
    return job(queue_name, connection=connection)(func)


@task
def execute_test(*, te_id=None, **kw):
    """
    Execute test via subprocess `pybot` and collect test report.
    """
    import subprocess as sp

    cmd = 'pybot mytest.robot'  # to be implemented
    proc = sp.Popen(f'{cmd}', shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    te = TestExecution.objects.get(pk=te_id)  # is it possible to send TestExecution obj?
    te.pybot_pid = proc.pid
    te.save()
    for line in proc.stdout:
        Pybot(pid=pybot_pid, output=line).save  # ordered by ID, and may have perf issue

    outs, errs = proc.communicate()
    assert outs == b''
    assert errs is None
    assert proc.returncode is not None

    collect_test_report()  # to be implemented

    return proc.returncode  # refer to `pybot` for return code meaning
