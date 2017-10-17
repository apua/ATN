import os
import tempfile

from robot.api import TestSuiteBuilder
from robot.api import ResultWriter
from robot.errors import DataError


def execute(test_data: str):
    """
    Execute test by single test suite in string.

    Use temporary file as a workaround, and only support log currently.
    """
    with tempfile.NamedTemporaryFile(suffix='.robot', delete=False) as fp:
        fp.write(test_data.encode())
    suite = TestSuiteBuilder().build(fp.name)
    result = suite.run(output=None, critical='rat')
    ResultWriter(result).write_results(report=None, log=fp.name)

    log = open(fp.name).read()

    os.unlink(fp.name)
    return log


if __name__=='__main__':
    try:
        result = execute('invalid content')
    except DataError as e:
        render = lambda e: {'message': e.message, 'details': e.details}
        result = render(e)
    print(result)
