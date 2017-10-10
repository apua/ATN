class TestData:
    r"""A workaround version input/output test data "model" with plain text.

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
    instances = {}
    last_id = 0

    def __init__(self, test_data):
        self.data = test_data

    def __del__(self):
        __class__.instances[self.id] = None

    def to_dict(self):
        return {'data': self.data}

    @staticmethod
    def add(testdata):
        __class__.last_id += 1
        __class__.instances[__class__.last_id] = testdata
        testdata.id = __class__.last_id
        return testdata.id

    def run(self):
        create_temporary_files()
        console = run_test_suite_via_subprocess()
        report, log, output = read_test_result()
        return {'report': report, 'log': log, 'output': output, 'console': console}


class ID(int):
    """Nothing but ID"""
