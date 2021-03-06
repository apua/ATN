"""
remote -> remote: create TE w/ start time, backup TD
remote -> local: TD source, remote TE ID [1]
local -> local: TE w/o backup, w/ remote TE id
local -> remote: local TE ID (i.e. RQ job ID) [2]
remote -> remote: TE update local TE ID

[1]
local -> local: TE is finished
local -> remote: POST TR w/ remote TE ID

[2]
remote -> local: by local TE ID, request a HTTP streaming for console
"""

import json

from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse

from . import tasks
from . models import ConsoleLine

@csrf_exempt
@require_POST
def execute_test(request):
    j = json.loads(request.body)
    #source = j['test_data']
    #command = f'pybot {source["filename"]}'
    #remote_id = j['remote_id']
    #host = j['host']
    #rq_job = tasks.execute_test.delay(td_src=source, cmd=command, rte_id=remote_id, taas=host)
    rq_job = tasks.execute_test.delay(td_dict=j)
    return JsonResponse({'rq_jid': rq_job.id})

@require_GET
def monitor_test_execution(request, rq_jid):
    from .models import TestExecution, TestResult
    from time import sleep

    def fetch_lines(te, last_id):
        cs = ConsoleLine.objects.filter(id__gt=last_id, test_execution=te,).order_by('id')
        lines = (c.output for c in cs)
        if cs:
            last_id = cs.last().id
        return last_id, lines

    def monitor(te, last_id=-1):
        while not TestResult.objects.filter(test_execution=te):
            last_id, lines = fetch_lines(te, last_id)
            yield from lines
            sleep(1)
        last_id, lines = fetch_lines(te, last_id)
        yield from lines

    te = TestExecution.objects.get(pk=rq_jid)
    trs = TestResult.objects.filter(test_execution=te)
    if trs:
        return HttpResponse(trs.first().console)
    else:
        return StreamingHttpResponse(monitor(te))


from django.utils.decorators import method_decorator
from django.views import View
from .models import Sut

@require_GET
def detail_sut(request, uuid):
    sut = Sut.objects.get(pk=uuid)
    return JsonResponse(sut.to_dict())

@csrf_exempt
@require_POST
def reserve_sut(request, uuid):
    j = json.loads(request.body)
    Sut.objects.get(pk=uuid).reserve(j['reserved_by'])
    return HttpResponse()

@csrf_exempt
@require_POST
def use_sut(request, uuid):
    j = json.loads(request.body)
    Sut.objects.get(pk=uuid).use(j['in_use'])
    return HttpResponse()

from .models import Taas

@method_decorator(csrf_exempt, name='dispatch')
class TaasView(View):
    def get(self, request):
        taas = Taas.objects.first()
        return JsonResponse({'ip': taas.ip, 'port': taas.port}) if taas else JsonResponse({})

    def put(self, request):
        """
        Mark test harness registered/unregistered
        """
        j = json.loads(request.body)
        if j:
            taas, created = Taas.objects.update_or_create(defaults=j)
        else:
            Taas.objects.all().delete()
            Sut.objects.filter(reserved_by__is_staff=False).update(reserved_by=None)
        return HttpResponse()

@require_GET
def list_suts(request):
    return JsonResponse(Sut.dump_all(), safe=False)


@require_GET
def test_report_page(requests, te_id, name):
    from .models import TestExecution, TestResult
    tr = TestExecution.objects.get(pk=te_id).test_result
    return HttpResponse(getattr(tr, name))
