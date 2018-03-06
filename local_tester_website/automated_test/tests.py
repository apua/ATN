import doctest
from django.test import TestCase

def load_tests(loader, tests, ignore):
    def doctest_it(mod_name):
        from importlib import import_module
        mod = import_module(f'.{mod_name}', __package__)
        tests.addTests(doctest.DocTestSuite(mod))

    doctest_it('models')
    doctest_it('tasks')
    return tests
