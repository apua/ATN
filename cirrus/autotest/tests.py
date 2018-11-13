import json
import textwrap
import unittest

import django.test

from .apps import AutotestConfig as Config


class RobotFramework(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        cls.origin_workspace = Config.workspace
        Config.workspace = Path('/tmp/unittest')

    @classmethod
    def tearDownClass(cls):
        Config.workspace = cls.origin_workspace

    def test_exec_via_pybot(self):
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


class RestApi(django.test.TestCase):
    test_data = textwrap.dedent("""\
            *** test cases ***
            T
                log to console  &{ilo}[ip]
            """)
    edited = textwrap.dedent("""\
            *** test cases ***
            T
                log to console  &{ilo}[ip]-edited
            """)
    suts = json.dumps({
        'ilo': {'ip': '10.30.1.3', 'username': 'administrator', 'password': 'password'}
        })

    def test_01_suite_api(self):
        """
        Test suite API
        """
        # suite list is empty
        response = self.client.get('/autotest/suites')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # create a suite
        payload = json.dumps({'content': self.test_data})
        response = self.client.post('/autotest/suites', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], '/autotest/suites/1')
        self.assertEqual(response.json(), {'id': 1})

        # suite list is not empty and can get the suite
        response = self.client.get('/autotest/suites')
        self.assertEqual(response.json(), [{'id': 1, 'content': self.test_data}])

        response = self.client.get('/autotest/suites/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'content': self.test_data})

        # update it and verify
        payload = json.dumps({'content': self.edited})
        response = self.client.put('/autotest/suites/1', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/autotest/suites/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'content': self.edited})

        # delete it and suite list is empty
        response = self.client.delete('/autotest/suites/1')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/autotest/suites')
        self.assertEqual(response.json(), [])

    def test_02_job_api(self):
        """
        Test job API with executing test suites
        """
        # create a suite
        payload = json.dumps({'content': self.test_data})
        response = self.client.post('/autotest/suites', data=payload, content_type='application/json')
        self.assertEqual(response.json(), {'id': 1})
        suite_id = response.json()['id']

        # job list is empty
        response = self.client.get('/autotest/jobs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # submit a job
        payload = json.dumps({'suite_id': suite_id, 'suts': self.suts})
        response = self.client.post('/autotest/jobs', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], '/autotest/jobs/1')
        self.assertEqual(response.json(), {'id': 1})

        # job list is not empty and can get job state and properties
        job = {'id': 1, 'suite_reference': suite_id, 'suite_content': self.test_data, 'suts': self.suts}

        response = self.client.get('/autotest/jobs')
        self.assertEqual(response.json(), [job])

        response = self.client.get('/autotest/jobs/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), job)

        # re-submit a test by its test suite and related suts
        response = self.client.post('/autotest/jobs/1', content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], '/autotest/jobs/2')
        self.assertEqual(response.json(), {'id': 2})
