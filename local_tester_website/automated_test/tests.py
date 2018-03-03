import doctest
from django.test import TestCase

def load_tests(loader, tests, ignore):
    from importlib import import_module
    for mod_name in ('tasks', 'models'):
        tests.addTests(doctest.DocTestSuite(
            import_module(f'.{mod_name}', __package__)
            ))
    return tests
