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


DEFAULT_TEST_DATA = json.dumps({
    'filename': 'basic.robot',
    'content': '*** test cases ***\nTC\n  log  message  console=yes\n',
    })


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_data = models.TextField(default=DEFAULT_TEST_DATA)  # TODO: validator
    last_modified = models.DateTimeField(auto_now=True)
    #refer_to = models.CharField(...)


class TestExecution(models.Model):
    rq_jid = models.UUIDField(primary_key=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.SET_NULL, null=True)
    origin = models.TextField(null=True)
    pid = models.PositiveSmallIntegerField(null=True)

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
    info = models.TextField()
    reserved_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
            related_name='reserved_sut', null=True, blank=True,
            )
    maintained_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
            related_name='maintained_sut',
            )

    @classmethod
    def dump_all(cls):
        return [
            {
                'uuid': sut.uuid,
                'info': sut.info,
                'reserved_by': None if sut.reserved_by is None else sut.reserved_by.email,
                'maintained_by': sut.maintained_by.email,
                }
            for sut in cls.objects.all()
            ]


class Taas(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    port = models.PositiveSmallIntegerField(default=80)
    # TODO: limit there is only one instance at most
