r"""

`TestExecution` use RQ queue ID an UUID as primary key::

    >>> from uuid import uuid4
    >>> rq_jid = uuid4()
    >>> te = TestExecution.objects.create(
    ...     pk=rq_jid,
    ...     test_data={},
    ...     )
    >>> assert te.pk == te.rq_jid

Don't insert bytes string into `output` char field::

    >>> from uuid import uuid4
    >>> rq_jid = uuid4()
    >>> te = TestExecution.objects.create(
    ...     pk=rq_jid,
    ...     test_data={},
    ...     )
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


from django.db import models


class TestExecution(models.Model):
    rq_jid = models.UUIDField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    test_data = models.TextField()
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
