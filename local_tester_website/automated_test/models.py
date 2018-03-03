from django.db import models


class TestExecution(models.Model):
    """
    id
    task_id
    pybot_pid
    """


class Pybot(models.Model):
    """
    id
    pid
    output
    """
