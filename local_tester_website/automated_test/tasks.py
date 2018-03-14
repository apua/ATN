r"""
This module implements method to "submit" and "stop" test execution.

Current test execution steps:

1.  Create a workspace
2.  Generate test data and put them into workspace
3.  Execute test with `pybot` (may be stopped during execution)
4.  Collect test report is existing

Call :func:`execute_test` directly::

    >>> td_src={
    ...     'filename': 'basic.robot',
    ...     'content': (
    ...         "*** test cases ***           \n"
    ...         "TC                           \n"
    ...         "    log  message  console=yes\n"
    ...         ),
    ...     }
    >>> te_pk, return_code = execute_test(
    ...     cmd=f'pybot -W 40 {td_src["filename"]}',
    ...     td_src=td_src,
    ...     )
    >>> assert return_code == 0

(cont.) Stored console output can be used on monitoring at Front-end::

    >>> from django.conf import settings
    >>> te = TestExecution.objects.get(pk=te_pk)
    >>> workdir = settings.ATN['WORKSPACE'] / str(te.start)
    >>> consoles = ConsoleLine.objects.filter(test_execution=te).order_by('id')
    >>> assert tuple(c.output for c in consoles) == (
    ...     '========================================\n',
    ...     'Basic                                   \n',
    ...     '========================================\n',
    ...     'TC                              message\n',
    ...     '| PASS |\n',
    ...     '----------------------------------------\n',
    ...     'Basic                           | PASS |\n',
    ...     '1 critical test, 1 passed, 0 failed\n',
    ...     '1 test total, 1 passed, 0 failed\n',
    ...     '========================================\n',
    ...    f'Output:  {workdir}/output.xml\n',
    ...    f'Log:     {workdir}/log.html\n',
    ...    f'Report:  {workdir}/report.html\n',
    ...     )

(cont.) test result contains full console output

    >>> assert te.test_result.console == (
    ...     '========================================\n'
    ...     'Basic                                   \n'
    ...     '========================================\n'
    ...     'TC                              message\n'
    ...     '| PASS |\n'
    ...     '----------------------------------------\n'
    ...     'Basic                           | PASS |\n'
    ...     '1 critical test, 1 passed, 0 failed\n'
    ...     '1 test total, 1 passed, 0 failed\n'
    ...     '========================================\n'
    ...    f'Output:  {workdir}/output.xml\n'
    ...    f'Log:     {workdir}/log.html\n'
    ...    f'Report:  {workdir}/report.html\n'
    ...     )


Submit a task and get RQ job::

    >>> td_src = {
    ...     'filename': 'submit.robot',
    ...     'content': (
    ...         "*** test cases ***\n"
    ...         "TC                \n"
    ...         "    sleep  5      \n"
    ...         ),
    ...     }
    >>> rq_job = execute_test.delay(
    ...     cmd=f'pybot {td_src["filename"]}',
    ...     td_src=td_src,
    ...     )
    >>> assert type(rq_job.id) is str
    >>> wait_until_task_finished(rq_job.id, timeout=6)

Stop a running job:

    >>> from time import sleep
    >>> td_src = {
    ...     'filename': 'stop.robot',
    ...     'content': (
    ...         "*** test cases ***\n"
    ...         "TC                \n"
    ...         "    sleep  5      \n"
    ...         ),
    ...     }
    >>> rq_job = execute_test.delay(
    ...     cmd=f'pybot {td_src["filename"]}',
    ...     td_src=td_src,
    ...     )
    >>> sleep(1)
    >>> stop_test_execution(rq_job.id)
    >>> wait_until_task_finished(rq_job.id, timeout=2)
"""


from .models import TestData, TestExecution, ConsoleLine, TestResult


def wait_until_task_finished(rq_jid: str, timeout):
    from time import sleep
    from rq.job import Job
    from redis import Redis
    from uuid import UUID

    job = Job.fetch(rq_jid, connection=Redis())
    for _ in range(timeout):
        sleep(1)
        if job.status == 'finished':
            break
    else:
        raise Exception(f'{job.status} is not finished after {timeout} seconds')


def stop_test_execution(te_pk: "str | UUID"):
    import os, signal, time

    pid = TestExecution.objects.get(pk=te_pk).pid
    assert pid is not None
    os.kill(pid, signal.SIGINT)


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
    #       -   `timeout`
    #           :default: None
    #
    #           The max job run time, it will kill `pybot` directly.
    #           Bad for generating test report.
    #
    #       -   `ttl`
    #           :default: None
    #
    #           The max job *queue* time.
    #
    #       -   `result_ttl`
    #           :default: 500
    #
    #           The expiration of stored job result.
    #           Unimportent obviously.
    return job(queue_name, connection=connection)(func)


@task
def execute_test(*, td_src=None, cmd=None, td_id=None, **kw):
    """
    Execute test via subprocess `pybot` and collect test report.
    """
    from pathlib import Path
    from uuid import uuid4, UUID
    import subprocess as sp

    from django.conf import settings
    from rq import get_current_job

    rq_job = get_current_job()
    rq_jid = uuid4() if rq_job is None else UUID(rq_job.id)
    assert type(rq_jid) is UUID

    if td_id is not None:
        td = TestData.objects.get(pk=td_id)
        te = TestExecution.objects.create(pk=rq_jid, test_data=td, origin=td.test_data)
    else:
        te = TestExecution.objects.create(pk=rq_jid)

    workdir = settings.ATN['WORKSPACE'] / str(te.start)
    workdir.mkdir(parents=True)
    with open(Path(workdir)/td_src['filename'], 'w') as f:
        f.write(td_src['content'])

    proc = sp.Popen(cmd, cwd=workdir, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    te.pid = proc.pid
    te.save(update_fields=['pid'])

    for line in proc.stdout:
        ConsoleLine.objects.create(test_execution=te, output=line.decode())

    outs, errs = proc.communicate()
    assert outs == b''
    assert errs is None
    assert proc.returncode is not None

    consoles = ConsoleLine.objects.filter(test_execution=te).order_by('id')
    TestResult.objects.create(
            test_execution=te,
            console=''.join(c.output for c in consoles),
            report=open(Path(workdir)/'report.html').read(),
            log=open(Path(workdir)/'log.html').read(),
            output=open(Path(workdir)/'output.xml').read(),
            )

    return te.pk, proc.returncode  # return code is defined by `pybot`
