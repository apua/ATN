import doctest
from django.test import TestCase

def load_tests(loader, tests, ignore):
    from . import tasks
    tests.addTests(doctest.DocTestSuite(tasks))
    return tests
