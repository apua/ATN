import uuid

from django.db import models
from django.conf import settings


class Harness(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(protocol='IPv4')
    def __str__(self): return self.ip.__str__()


class Sut(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    harness = models.ForeignKey(Harness, on_delete=models.CASCADE)
    oobm = models.TextField()
    def __str__(self): return self.oobm.__str__()


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
