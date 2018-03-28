r"""
`TestExecution` use RQ queue ID an UUID as primary key::

    >>> from uuid import uuid4
    >>> rq_jid = uuid4()
    >>> te = TestExecution.objects.create(
    ...     pk=rq_jid,
    ...     origin=DEFAULT_TEST_DATA,
    ...     )
    >>> assert te.pk == te.rq_jid

(conti.) Don't insert bytes string into `output` char field::

    >>> pb = ConsoleLine.objects.create(test_execution=te, output='')

    >>> pb.output = b'3 critical tests, 3 passed, 0 failed'
    >>> pb.output
    b'3 critical tests, 3 passed, 0 failed'
    >>> pb.save() ; pb.refresh_from_db()
    >>> pb.output
    "b'3 critical tests, 3 passed, 0 failed'"

    >>> pb.output = b'3 critical tests, 3 passed, 0 failed'.decode()
    >>> pb.output
    '3 critical tests, 3 passed, 0 failed'
    >>> pb.save() ; pb.refresh_from_db()
    >>> pb.output
    '3 critical tests, 3 passed, 0 failed'
"""


import json
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


DEMO_SUITE = """\
*** Test Cases ***
TC
    log  ${DEMO_VAR}  console=yes
    log  ${SUTs}      console=yes
"""
DEMO_VARIABLES = """\
DEMO_VAR: demo variable
"""
User = get_user_model()


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    suite = models.TextField(default=DEMO_SUITE)
    vars = models.TextField(default=DEMO_VARIABLES)
    suts = models.ManyToManyField('Sut', blank=True)

    def is_executable_by(self, user) -> bool:
        # TODO: define to handle different exceptions
        return (
                user == self.author
                and all(user == sut.reserved_by for sut in self.suts.all())
                and all(not sut.in_use for sut in self.suts.all())
                )

    def gen_suts_data(self) -> 'pybot variablefile':
        return json.dumps({'SUTs': {sut.name: sut.info for sut in self.suts.all()}})

    def gen_pybot_command(self, variable_files=('suts.yaml', 'vars.yaml'), suite='suite.robot'):
        return f'pybot {" ".join(f"-V {fn}" for fn in variable_files)} {suite}'

    def submit_test_execution(self) -> 'rq_job':
        from .tasks import execute_test
        rq_job = execute_test.delay(td_id=self.id)
        return rq_job

    def backup(self) -> str:
        return json.dumps({
            'suite': self.suite,
            'variables': self.vars,
            'SUTs': {sut.name: sut.info for sut in self.suts.all()},  # TODO: restrict `sut.info` type
            })


class TestExecution(models.Model):
    rq_jid = models.UUIDField(primary_key=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.SET_NULL, null=True)
    suts = models.ManyToManyField('Sut', blank=True)
    backup = models.TextField(null=True)
    pid = models.PositiveSmallIntegerField(null=True)

    def is_job_finished(self) -> bool:
        from redis import Redis
        from rq.job import Job
        from rq.exceptions import NoSuchJobError
        try:
            job = Job.fetch(rq_jid, connection=Redis())
        except NoSuchJobError:
            return True
        else:
            return job.status == 'finished'

    def submit(*a, **kw): ...
    def stop(*a, **kw): ...
    def get_console(*a, **kw): ...


class ConsoleLine(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE)
    output = models.CharField(max_length=256, default=None)


class TestResult(models.Model):
    test_execution = models.OneToOneField(TestExecution, on_delete=models.CASCADE, related_name='test_result')
    console = models.TextField()
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()

    def to_dict(self):
        return {
                "console": self.console,
                "report": self.report,
                "log": self.log,
                "output": self.output,
                }

    def upload(self, to_uri):
        import requests
        resp = requests.put(to_uri, json=self.to_dict())
        # TODO: `upload` or say `post script`?
        # NOTE: it`s a workaround
        sut_ids = requests.get(to_uri.replace('test-reporting', 'test-execution')).json()['suts']
        taas = Taas.objects.first()
        for sid in sut_ids:
            sut = Sut.objects.get(pk=sid)
            sut.in_use = False ; sut.save()
            requests.put(
                    f'http://{taas}/sut/{sut.uuid}/',
                    json=sut.to_dict(),
                    )
            print(f'sut_uuid -> {sid}')
        assert resp.status_code == 200


def gen_name():
    from time import time
    return f'name{int(time())}'


class Sut(models.Model):
    """
    Info example::

        UUID: 32353537-3036-4E43-3734-353230353447
        Server Serial Number: CN7452054G
        Product ID: 755260-AA1
        Product Name: ProLiant DL360 Gen9
        IP Address: 10.30.170.120
        Login Name: administrator
        Password:

    Maintainer example::

        nancy@hpe.com
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, default=gen_name)
    info = models.TextField()
    reserved_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
            related_name='reserved_sut', null=True, blank=True,
            )
    maintained_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
            related_name='maintained_sut',
            )
    in_use = models.BooleanField(default=False)

    @classmethod
    def dump_all(cls):
        return [sut.to_dict() for sut in cls.objects.all()]

    def use(self, in_use):
        self.in_use = in_use
        self.save(update_fields=['in_use'])

    def reserve(self, reserved_by):
        self.reserved_by, created = (None, False) if reserved_by is None else User.objects.get_or_create(
                email=reserved_by,
                defaults={'username': reserved_by},
                )
        self.save(update_fields=['reserved_by'])

    def to_dict(self):
        return {
                'uuid': str(self.uuid),
                'name': self.name,
                'info': self.info,
                'reserved_by': self.reserved_by and self.reserved_by.email,
                'maintained_by': self.maintained_by.email,
                'in_use': self.in_use,
                }


class Taas(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    port = models.PositiveSmallIntegerField(default=8000)
    # TODO: limit there is only one instance at most

    def __str__(self):
        return f'{self.ip}:{self.port}'
