import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings

from .models import TestHarness, Sut, TestResult


@csrf_exempt
@require_http_methods(['PUT'])
def upload_test_reporting(request, te_id):
    j = json.loads(request.body)
    TestResult.objects.create(
            test_execution_id=te_id,
            console=j['console'],
            report=j['report'],
            log=j['log'],
            output=j['output'],
            )
    return HttpResponse()


from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class SutView(View):
    def get(self, request, uuid):
        sut = Sut.objects.get(pk=uuid)
        return JsonResponse(sut.to_json())

    def put(self, request, uuid):
        j = json.loads(request.body)
        Sut.update_or_create(uuid, j)
        return HttpResponse()


from django.views.decorators.http import require_GET
from django.http import StreamingHttpResponse

@require_GET
def detail_test_execution(request, te_id):
    from .models import TestExecution
    return JsonResponse(TestExecution.objects.get(pk=te_id).to_dict())

@require_GET
def test_execution(request, rq_jid):
    import requests
    from .models import TestExecution
    query_string = request.META['QUERY_STRING']
    if not TestExecution.objects.get(rq_jid=rq_jid).suts.exists(): return HttpResponse()  # TODO: legacy
    harness = TestExecution.objects.get(rq_jid=rq_jid).suts.first().harness
    r = requests.get(
                f'http://{harness}/test-execution/{rq_jid}/console/',
                stream=True,
                )
    try:
        r.raise_for_status()
    except:
        return HttpResponse()
    else:
        return StreamingHttpResponse(
            f'{line}\n'
            for line in r.iter_lines(chunk_size=1, decode_unicode=True)
            )


@require_GET
def test_report_page(requests, te_id, name):
    from .models import TestExecution, TestResult
    tr = TestExecution.objects.get(pk=te_id).test_result
    return HttpResponse(getattr(tr, name))
