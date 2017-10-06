from hug import get, post, put, delete
import hug


class TestData:
    r"""
    A workaround version input/output test data "model" with plain text

    A test data includes:

    - test library
    - test suite
      - test case
      - variables
      - keywords
    - resource and variable files (for sharing)

    It is recursive in JSON, eg:

    >>> test_data = TestData({
    ...     'top_level': {  # suite folder name
    ...         '__init__.robot': '***settings***\nresource resource.robot\nsuite setup  init\n',
    ...         '2__suite.robot': '***test cases***\n1st Case\n    log_to_console  suite 2\n',
    ...         '1__suite.robot': '***test cases***\n1st Case\n    log_to_console  suite 1\n',
    ...         'resource.robot': '***keywords***\ninit\n    log_to_console  init lol\n',
    ...         }
    ...     })
    """
    def __init__(self, test_data):
        self.data = test_data

    def run(self):
        create_temporary_files()
        console = run_test_suite_via_subprocess()
        report, log, output = read_test_result()
        return {'report': report, 'log': log, 'output': output, 'console': console}


@get('/')
def list():
    return [1,2,3]


@get('/{id}')
def _(id: int):
    return f'content of test case {id}'


@post('/')
def _(testcase: TestCase):
    return f'generate id with testcase {testcase}'


@put('/{id}')
def _(id: int, body):
    return f'{id} - {body}'


@delete('/{id}')
def f(id: int):
    pass
