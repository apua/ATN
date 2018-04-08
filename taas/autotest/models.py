import json
import uuid

from django.db import models
from django.conf import settings
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


class TestHarness(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    port = models.PositiveSmallIntegerField(default=80)

    def __str__(self):
        return f'{self.ip}:{self.port}'


class Sut(models.Model):
    uuid = models.UUIDField(primary_key=True)
    harness = models.ForeignKey(TestHarness, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
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
    def load_all(cls, th, suts):
        cls.objects.bulk_create([
            cls(
                uuid=sut['uuid'],
                name=sut['name'],
                info=sut['info'],
                harness=th,
                reserved_by=None if sut['reserved_by'] is None else User.objects.get(email=sut['reserved_by']),
                maintained_by=User.objects.get(email=sut['maintained_by']),
                )
            for sut in suts
            ])

    @classmethod
    def update_or_create(cls, uuid, j):
        print(j)
        if not j.get('harness'):  # NOTE: it's workaround
            return Sut.objects.filter(pk=uuid).update(
                name=j['name'],
                info=j['info'],
                reserved_by=None if j['reserved_by'] is None else User.objects.get(email=j['reserved_by']),
                maintained_by=User.objects.get(email=j['maintained_by']),
                in_use=j['in_use'],
                )

        return Sut.objects.update_or_create(pk=uuid, defaults={
                'name': j['name'],
                'info': j['info'],
                'harness': TestHarness.objects.get(**j['harness']),
                'reserved_by': None if j['reserved_by'] is None else User.objects.get(email=j['reserved_by']),
                'maintained_by': User.objects.get(email=j['maintained_by']),
                'in_use': j['in_use'],
                })

    def to_json(self):
        return {
                'uuid': self.uuid,
                'harness': self.harness.ip,
                'name': self.name,
                'info': self.info,
                'reserved_by': self.reserved_by and self.reserved_by.email,
                'maintained_by': self.maintained_by and self.maintained_by.email,
                'in_use': j['in_use'],
                }


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    suite = models.TextField(default=DEMO_SUITE)
    vars = models.TextField(default=DEMO_VARIABLES)
    suts = models.ManyToManyField('Sut', blank=True)

    def is_executable_by(self, user):
        """
        #.  user == author
        #.  suts are at the same harness
        #.  suts are reserved 
        #.  send to harness to validate whether executable or not
        """
        return (
                user == self.author
                and self.suts.values_list('harness').count() == 1
                and self.suts.exclude(reserved_by=user).count() == 0
                and self.suts.filter(in_use=True).count() == 0
                )

    def submit_test_execution(self) -> 'rq_jid':
        import requests
        te = TestExecution.objects.create(
                #pk=rq_jid,
                test_data=self,
                backup=self.backup(),
                )
        te.suts.set(self.suts.all())
        te.suts.update(in_use=True)
        for sut in te.suts.all():
            requests.post(f'http://{self.suts.first().harness}/sut/{sut.pk}/use/', json={'in_use': True})

        r = requests.post(f'http://{self.suts.first().harness}/test-execution/', json={
            'suite': self.suite,
            'suts': self.gen_suts_data(),
            'vars': self.vars,
            'id': te.id,
            })
        r.raise_for_status()

        te.rq_jid = r.json()['rq_jid']
        te.save(update_fields=['rq_jid'])
        return te.rq_jid

    def gen_suts_data(self) -> 'pybot variablefile':
        return json.dumps({'SUTs': {sut.name: sut.info for sut in self.suts.all()}})

    def backup(self) -> str:
        return json.dumps({
            'suite': self.suite,
            'variables': self.vars,
            'SUTs': {sut.name: sut.info for sut in self.suts.all()},
            })


class TestExecution(models.Model):
    rq_jid = models.UUIDField(null=True, blank=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.SET_NULL, null=True)
    suts = models.ManyToManyField('Sut', blank=True)
    backup = models.TextField(null=True)

    def to_dict(self):
        return {
                'id': self.pk,
                'rq_jid': str(self.rq_jid),
                'start': self.start.timestamp(),
                'test_data': self.test_data.pk,
                'suts': [str(sut.pk) for sut in self.suts.all()],
                'backup': self.backup,
                }

class TestResult(models.Model):
    test_execution = models.OneToOneField(TestExecution, on_delete=models.CASCADE, related_name='test_result')
    console = models.TextField()
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()
