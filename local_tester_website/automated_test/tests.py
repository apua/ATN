from doctest import DocTestSuite
from importlib import import_module


MODULE_NAMES = ('models', 'tasks')

doctest_suites = {
       mod_name: DocTestSuite(import_module(f'.{mod_name}', __package__))
       for mod_name in MODULE_NAMES
       }
globals().update(doctest_suites)


def load_tests(loader, tests, ignore):
    for suite in doctest_suites.values():
        tests.addTests(suite)
    return tests
