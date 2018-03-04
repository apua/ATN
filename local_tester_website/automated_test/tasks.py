r"""
This module implements method to "submit" and "stop" test execution.

Current test execution steps:

1.  Create a workspace
2.  Generate test data and put them into workspace
3.  Execute test with `pybot` (may be stopped during execution)
4.  Collect test report is existing

::

    >>> from pathlib import Path
    >>> WORKSPACE = '.'  # TODO: define :const:`WORKSPACE`
    >>> workspace = Path.cwd() / WORKSPACE

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
    ...         'report': ('report.html', 'log.html', 'output.xml'),
    ...         },
    ...     wsp=f'{workspace}',
    ...     )
    >>> return_code
    0

Stored console output may be used on monitoring at Front-end::

    >>> te = TestExecution.objects.get(pk=te.id)
    >>> po = Pybot.objects.filter(pid=te.pybot_pid).order_by('id')
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
    ...    f'Output:  {workspace}/output.xml\n',
    ...    f'Log:     {workspace}/log.html\n',
    ...    f'Report:  {workspace}/report.html\n',
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
    ...     'report': ('report.html', 'log.html', 'output.xml'),
    ...     }
    >>> te = submit_test_execution(td_src)

(conti.) Monitor job status till "finished" (time out after 10 seconds)::

    >>> from time import sleep
    >>> from rq.job import Job
    >>> from redis import Redis
    >>> job = Job.fetch(te.task_id, connection=Redis())
    >>> for _ in range(10):
    ...     sleep(1)
    ...     if job.status == 'finished':
    ...         break
    ... else:
    ...     raise AssertionError(f'{job.status} not finished')

Stop a running job (time out after 3 seoncds):

    >>> from time import sleep
    >>> td_src = {
    ...     'filename': 'doctest.robot',
    ...     'content': (
    ...         "*** test cases ***\n"
    ...         "TC                \n"
    ...         "    sleep  5      \n"
    ...         ),
    ...     'report': ('report.html', 'log.html', 'output.xml'),
    ...     }
    >>> te_id = submit_test_execution(td_src).id
    >>> sleep(1)
    >>> stop_test_execution(te_id, timeout=3)
"""


from .models import TestExecution, Pybot


def stop_test_execution(te_id, timeout):
    import os, signal, time

    pid = TestExecution.objects.get(pk=te_id).pybot_pid
    os.kill(pid, signal.SIGINT)
    for _ in range(3):
        time.sleep(1)
        try: os.kill(pid, 0)
        except OSError: break
    else:
        raise OSError(f'cannot kill pid {pid}')


def submit_test_execution(td_src: dict) -> TestExecution:
    te = TestExecution.objects.create()
    rq_job = execute_test.delay(
            te_id=te.id, td_src=td_src, wsp='.',
            cmd=f'pybot {td_src["filename"]}'
            )
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
def execute_test(*, te_id=None, td_src=None, wsp=None,
                 cmd='pybot mytest.robot', **kw):
    """
    Execute test via subprocess `pybot` and collect test report.
    """
    import subprocess as sp

    # Setup
    generate_test_data(test_data_source=td_src, workspace=wsp)

    # Execution
    proc = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    # TODO: is it possible to send TestExecution obj?
    te = TestExecution.objects.get(pk=te_id)
    te.pybot_pid = proc.pid
    te.save()
    for line in proc.stdout:
        # TODO: ordered by ID, and may have perf issue
        Pybot.objects.create(pid=te.pybot_pid, output=line.decode())

    outs, errs = proc.communicate()
    assert outs == b''
    assert errs is None
    assert proc.returncode is not None

    # Teardown
    #assert test_report_exist()  # to be implemented
    collect_test_report(test_data_source=td_src, workspace=wsp)  # to be implemented

    return proc.returncode  # refer to `pybot` for return code meaning


def generate_test_data(test_data_source, workspace):
    # TODO: improve API
    import os
    os.chdir(workspace)
    with open(test_data_source['filename'], 'w') as f:
        f.write(test_data_source['content'])


def collect_test_report(test_data_source, workspace):
    # TODO: improve API
    import os
    os.chdir(workspace)
    for filename in test_data_source['report']:
        os.remove(filename)
    os.remove(test_data_source['filename'])
