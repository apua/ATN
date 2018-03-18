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

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import tasks

@csrf_exempt
@require_POST
def execute_test(request):
    j = json.loads(request.body)
    source = j['test_data']
    command = f'pybot {source["filename"]}'
    remote_id = j['remote_id']
    rq_job = tasks.execute_test.delay(td_src=source, cmd=command, rte_id=remote_id)
    return JsonResponse({'rq_jid': rq_job.id})
