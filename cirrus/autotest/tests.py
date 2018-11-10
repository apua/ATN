import unittest

import django.test as django

from .apps import AutotestConfig as Config


class RF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        cls.origin_workspace = Config.workspace
        Config.workspace = Path('/tmp/unittest')

    @classmethod
    def tearDownClass(cls):
        Config.workspace = cls.origin_workspace

    def test_exec_via_pybot(self):
        import textwrap
        from . import rf
        suite = textwrap.dedent("""\
                *** test cases ***
                T
                    log to console  &{ilo}[ip]
                """)
        suts = {'ilo': {'ip':'10.30.3.1','username':'root','password':'Compaq123'}}
        with rf.exec_via_pybot(dirname='mvp', suite=suite, suts=suts) as proc:
            #print('PID:', proc.pid)
            #print(*('=> ' + line.decode() for line in proc.stdout), sep='')
            list(proc.stdout)
        assert proc.returncode == 0

    def test_async_testexec(self):
        from . import rf, rq
        rq_job = rf.exec_test.delay()
        assert type(rq_job.id) is str
        rq.wait_for_finished(rq_job.id, timeout=3)
        returncode = rq_job.result
        assert returncode == 0


class App(django.TestCase):
    pass
