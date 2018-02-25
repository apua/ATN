import uuid

from django.db import models
from django.conf import settings


class Harness(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(protocol='IPv4')


class Sut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)

    #from django.contrib.postgres.fields import JSONField
    #oobm = models.JSONField()


class Reservation(models.Model):
    sut = models.ForeignKey(Sut, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class TestData(models.Model):
    settings = models.TextField()
    variables = models.TextField()
    test_cases = models.TextField()
    keywords = models.TextField()


class TestExecution(models.Model):
    test_data = models.ForeignKey(TestData, on_delete=models.CASCADE)
    sut = models.ForeignKey(Sut, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    test_report = models.FileField()
    #test_report = models.FileField(upload_to='uploads/')
