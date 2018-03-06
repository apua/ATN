r"""

Create instance and save to database in one line::

    >>> #TestExecution().save()
    >>> te = TestExecution.objects.create()

Get by `id` field or `pk` argument::

    >>> assert TestExecution.objects.get(id=te.id) \
    ...     == TestExecution.objects.get(pk=te.id)
    >>> assert TestExecution.objects.get(id=te.id) \
    ...     is not TestExecution.objects.get(pk=te.id)

Arguments `pid` and `output` are required::

    >>> Pybot.objects.create()
    Traceback (most recent call last):
        ...
    django.db.utils.IntegrityError: NOT NULL constraint failed: automated_test_pybot.pid
    >>> Pybot.objects.create(pid=9487)
    Traceback (most recent call last):
        ...
    django.db.utils.IntegrityError: NOT NULL constraint failed: automated_test_pybot.output

Note that don't insert bytes string into `output` char field::

    >>> line = b'3 critical tests, 3 passed, 0 failed'
    >>> pb1 = Pybot.objects.create(pid=9487, output=line)
    >>> pb1.output
    b'3 critical tests, 3 passed, 0 failed'
    >>> pb2 = Pybot.objects.get(pk=pb1.id)
    >>> pb2.output
    "b'3 critical tests, 3 passed, 0 failed'"
    >>> pb3 = Pybot.objects.create(pid=9487, output=line.decode())
    >>> pb3 = Pybot.objects.get(pk=pb3.id)
    >>> pb3.output
    '3 critical tests, 3 passed, 0 failed'
"""


from django.db import models


class TestExecution(models.Model):
    task_id = models.UUIDField(null=True)
    pybot_pid = models.PositiveSmallIntegerField(null=True)


class Pybot(models.Model):
    pid = models.PositiveSmallIntegerField()
    output = models.CharField(max_length=256, default=None)
