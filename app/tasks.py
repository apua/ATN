from celery import Celery


queue = Celery('A___________A', backend='rpc://', broker='pyamqp://')


@queue.task
def submit(suite_id):
    import robot
    from .couch_wrap import get_suite, new_result, put2db

    suite = get_suite(suite_id)
    try:
        log_html = execute(suite.data)
    except robot.erros.DataError as e:
        import traceback
        log_html = f'<pre>{ "".join(traceback.format_exc()) }</pre>'
    put2db(new_result(log_html, suite.id, suite.rev))


def execute(test_data: str):
    """
    Execute test by single test suite in string.

    Use temporary file as a workaround, and only support log currently.
    """
    import os, tempfile
    from robot.api import TestSuiteBuilder, ResultWriter

    with tempfile.NamedTemporaryFile(suffix='.robot', delete=False) as fp:
        fp.write(test_data.encode())
    suite = TestSuiteBuilder().build(fp.name)
    result = suite.run(output=None, critical='rat')
    ResultWriter(result).write_results(report=None, log=fp.name)

    log = open(fp.name).read()

    os.unlink(fp.name)
    return log
