import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings

from .models import TestHarness, Sut, TestResult


@csrf_exempt
@require_POST
def upload_testresult(request):
    j = json.loads(request.body)
    TestResult.objects.create(
            test_execution_id=j['test_execution_id'],
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
        return JsonResponse({
                'uuid': sut.uuid,
                'harness': sut.harness.ip,
                'credential': sut.credential,
                'reserved_by': sut.reserved_by and sut.reserved_by.email,
                'maintained_by': sut.maintained_by and sut.maintained_by.email,
                })

    def put(self, request, uuid):
        j = json.loads(request.body)
        sut, created = Sut.update_or_create(j)
        return HttpResponse()


from django.views.decorators.http import require_GET
from django.http import StreamingHttpResponse

@require_GET
def test_execution(request, rq_jid):
    from requests import get
    query_string = request.META['QUERY_STRING']
    return StreamingHttpResponse(
            f'{line}\n'
            for line in get(
                NotImplemented,
                #f'http://127.0.0.1:2345/testexecution/{rq_jid}?{query_string}',
                stream=True,
                ).iter_lines(chunk_size=1, decode_unicode=True)
            )
