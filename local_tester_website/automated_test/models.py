r"""
Don't insert bytes string into `output` char field::

    >>> te = TestExecution.objects.create()
    >>> pb = Pybot.objects.create(test_execution=te, output='')

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
    # TODO: ideally, ...
    #    - require `test_data` field
    #    - has `submit` method
    #    - has `stop` method
    #    - has `get_console` method
    test_data = models.TextField(null=True)
    task_id = models.UUIDField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    pybot_pid = models.PositiveSmallIntegerField(null=True)


class Pybot(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE)
    output = models.CharField(max_length=256, default=None)


class TestResult(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE)
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()
