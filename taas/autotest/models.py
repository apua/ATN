import json
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


DEFAULT_TEST_DATA = json.dumps({
    'filename': 'basic.robot',
    'content': '*** test cases ***\nTC\n  log  message  console=yes\n',
    })
User = get_user_model()


class TestHarness(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    port = models.PositiveSmallIntegerField(default=80)


class Sut(models.Model):
    uuid = models.UUIDField(primary_key=True)
    harness = models.ForeignKey(TestHarness, on_delete=models.CASCADE)
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
    def load_all(cls, th, suts):
        cls.objects.bulk_create([
            cls(
                uuid=sut['uuid'],
                info=sut['info'],
                harness=th,
                reserved_by=None if sut['reserved_by'] is None else User.objects.get(email=sut['reserved_by']),
                maintained_by=User.objects.get(email=sut['maintained_by']),
                )
            for sut in suts
            ])

    @classmethod
    def update_or_create(cls, j):
        sut, created = Sut.objects.update_or_create(pk=uuid, defaults={
                'info': j['info'],
                'harness': TestHarness.objects.get(**j['harness']),
                'reserved_by': None if j['reserved_by'] is None else User.objects.get(email=j['reserved_by']),
                'maintained_by': User.objects.get(email=j['maintained_by']),
                })

    def to_json(self):
        return {
                'uuid': self.uuid,
                'harness': self.harness.ip,
                'info': self.info,
                'reserved_by': self.reserved_by and self.reserved_by.email,
                'maintained_by': self.maintained_by and self.maintained_by.email,
                }


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_data = models.TextField(default=DEFAULT_TEST_DATA)
    last_modified = models.DateTimeField(auto_now=True)
    #refer_to = models.CharField(...)


class TestExecution(models.Model):
    rq_jid = models.UUIDField(null=True, blank=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.SET_NULL, null=True)
    origin = models.TextField(null=True)


class TestResult(models.Model):
    test_execution = models.OneToOneField(TestExecution, on_delete=models.CASCADE, related_name='test_result')
    console = models.TextField()
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()
