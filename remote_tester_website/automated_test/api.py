import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings

from .models import ExecLayer, Sut, TestResult


def get_user_or_none_by_email(email):
    from django.contrib.auth.models import User
    try:
        return User.objects.get(email=email)
    except Exception as e:
        print(e.args)
        return None


@csrf_exempt
@require_POST
def register(request):
    print(request.body)
    j = json.loads(request.body)
    ex = ExecLayer.objects.create(ip=j['ip'])
    for s in j['suts']:
        Sut.objects.create(
                uuid=s['uuid'],
                exec_layer=ex,
                reserved_by=get_user_or_none_by_email(s['reserved_by']),
                maintained_by=get_user_or_none_by_email(s['maintained_by']),
                )
    return JsonResponse({'id': ex.id})


@csrf_exempt
@require_http_methods(['DELETE'])
def unregister(request, id):
    ex = ExecLayer.objects.get(id=id)
    Sut.objects.filter(exec_layer=ex).delete()
    ex.delete()
    return HttpResponse()


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
                'exec_layer': sut.exec_layer.ip,
                'credential': sut.credential,
                'reserved_by': sut.reserved_by and sut.reserved_by.email,
                'maintained_by': sut.maintained_by and sut.maintained_by.email,
                })

    def put(self, request, uuid):
        j = json.loads(request.body)
        sut = Sut.objects.get(pk=uuid)
        sut.reserved_by = get_user_or_none_by_email(j['reserved_by'])
        sut.maintained_by = get_user_or_none_by_email(j['maintained_by'])
        sut.save(update_fields=['reserved_by', 'maintained_by'])
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
                f'http://127.0.0.1:8000/testexecution/{rq_jid}?{query_string}',
                stream=True,
                ).iter_lines(chunk_size=1, decode_unicode=True)
            )
