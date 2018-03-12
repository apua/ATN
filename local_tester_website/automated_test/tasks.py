r"""
This module implements method to "submit" and "stop" test execution.

Current test execution steps:

1.  Create a workspace
2.  Generate test data and put them into workspace
3.  Execute test with `pybot` (may be stopped during execution)
4.  Collect test report is existing

Call :func:`execute_test` directly::

    >>> te = TestExecution.objects.create()
    >>> return_code = execute_test(
    ...     te_id=te.id,
    ...     cmd='pybot -W 40 doctest.robot',
    ...     td_src={
    ...         'filename': 'doctest.robot',
    ...         'content': (
    ...             "*** test cases ***           \n"
    ...             "TC                           \n"
    ...             "    log  message  console=yes\n"
    ...             ),
    ...         },
    ...     )
    >>> return_code
    0

Stored console output may be used on monitoring at Front-end::

    >>> from django.conf import settings
    >>> te = TestExecution.objects.get(pk=te.id)
    >>> workdir = settings.ATN['WORKSPACE'] / str(te.created)
    >>> po = Pybot.objects.filter(test_execution=te).order_by('id')
    >>> assert tuple(pl.output for pl in po) == (
    ...     '========================================\n',
    ...     'Doctest                                 \n',
    ...     '========================================\n',
    ...     'TC                              message\n',
    ...     '| PASS |\n',
    ...     '----------------------------------------\n',
    ...     'Doctest                         | PASS |\n',
    ...     '1 critical test, 1 passed, 0 failed\n',
    ...     '1 test total, 1 passed, 0 failed\n',
    ...     '========================================\n',
    ...    f'Output:  {workdir}/output.xml\n',
    ...    f'Log:     {workdir}/log.html\n',
    ...    f'Report:  {workdir}/report.html\n',
    ...     )
    >>> # TODO: consider fetching log continuous;
    >>> #       in other words, consider perf issue of fetching partial log
    >>> # TODO: rename "Pybot" to "ConsoleLine"

Submit a task (sleep 5 seconds)::

    >>> td_src = {
    ...     'filename': 'doctest.robot',
    ...     'content': (
    ...         "*** test cases ***\n"
    ...         "TC                \n"
    ...         "    sleep  5      \n"
    ...         ),
    ...     }
    >>> te_id = submit_test_execution(td_src)
    >>> task_id = TestExecution.objects.get(pk=te_id).task_id.__str__()
    >>> wait_until_task_finished(task_id, timeout=6)

Stop a running job:

    >>> from time import sleep
    >>> td_src = {
    ...     'filename': 'doctest.robot',
    ...     'content': (
    ...         "*** test cases ***\n"
    ...         "TC                \n"
    ...         "    sleep  5      \n"
    ...         ),
    ...     }
    >>> te_id = submit_test_execution(td_src)
    >>> sleep(1)
    >>> stop_test_execution(te_id)
    >>> task_id = TestExecution.objects.get(pk=te_id).task_id.__str__()
    >>> wait_until_task_finished(task_id, timeout=2)
"""


from .models import TestExecution, Pybot, TestResult


def wait_until_task_finished(task_id: str, timeout):
    from time import sleep
    from rq.job import Job
    from redis import Redis

    job = Job.fetch(task_id, connection=Redis())
    for _ in range(timeout):
        sleep(1)
        if job.status == 'finished':
            break
    else:
        raise Exception(f'{job.status} is not finished')


def stop_test_execution(te_id):
    import os, signal, time

    pid = TestExecution.objects.get(pk=te_id).pybot_pid
    assert pid is not None
    os.kill(pid, signal.SIGINT)


def submit_test_execution(td_src: dict) -> TestExecution:
    te = TestExecution.objects.create()
    rq_job = execute_test.delay(
            te_id=te.id, td_src=td_src,
            cmd=f'pybot {td_src["filename"]}'
            )
    TestExecution.objects.filter(pk=te.id).update(task_id=rq_job.id)
    assert type(rq_job.id) is str
    return te.id


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
def execute_test(*, te_id=None, td_src=None, cmd=None, **kw):
    """
    Execute test via subprocess `pybot` and collect test report.
    """
    from pathlib import Path
    import subprocess as sp

    from django.conf import settings

    te = TestExecution.objects.get(pk=te_id)
    workdir = settings.ATN['WORKSPACE'] / str(te.created)

    workdir.mkdir(parents=True)
    with open(Path(workdir)/td_src['filename'], 'w') as f:
        f.write(td_src['content'])

    proc = sp.Popen(cmd, cwd=workdir, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    TestExecution.objects.filter(pk=te.id).update(pybot_pid=proc.pid)

    for line in proc.stdout:
        # TODO: ordered by ID, and may have perf issue
        Pybot.objects.create(test_execution=te, output=line.decode())

    outs, errs = proc.communicate()
    assert outs == b''
    assert errs is None
    assert proc.returncode is not None

    TestResult.objects.create(
            test_execution=te,
            report=open(Path(workdir)/'report.html').read(),
            log=open(Path(workdir)/'log.html').read(),
            output=open(Path(workdir)/'output.xml').read(),
            )

    return proc.returncode  # refer to `pybot` for return code meaning
