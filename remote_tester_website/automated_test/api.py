import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings

from .models import ExecLayer, Sut


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
