import json

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import reverse as urls_reverse

from .models import Suite, Job


class SuiteCollectionView(View):
    """
    View of suite collection

    - GET for suites list (may with pagination or filtering in future implement)
    - POST to add new suite
    """
    def get(self, request):
        return JsonResponse(Suite.objects.to_list(), safe=False)

    def post(self, request):
        payload = json.loads(request.body.decode())
        suite = Suite.objects.create(content=payload['content'])
        response = JsonResponse({'id': suite.id}, status=201)
        response['Location'] = urls_reverse('autotest:suite', args=(suite.id,))
        return response


class SuiteView(View):
    """
    View of a suite

    - GET for a suite content
    - PUT to edit a suite
    - DELETE to remove a suite (or archive it in future implement)
    """
    def get(self, request, id):
        return JsonResponse(Suite.objects.get(id=id).to_dict())

    def put(self, request, id):
        payload = json.loads(request.body.decode())
        Suite.objects.filter(id=id).update(content=payload['content'])
        return HttpResponse(status=204)

    def delete(self, request, id):
        Suite.objects.get(id=id).delete()
        return HttpResponse(status=204)


class JobCollectionView(View):
    """
    View of job collection

    - GET for jobs list (may with pagination or filtering in future implement)
    - POST to submit a job with a test suite and suts
    """
    def get(self, request):
        return JsonResponse(Job.objects.to_list(), safe=False)

    def post(self, request):
        payload = json.loads(request.body.decode())
        suite_id = payload['suite_id']
        suts = payload['suts']
        suite_content = Suite.objects.get(id=suite_id).content
        job = Job.objects.create(suite_reference_id=suite_id, suite_content=suite_content, suts=suts)
        response = JsonResponse({'id': job.id}, status=201)
        response['Location'] = urls_reverse('autotest:job', args=(job.id,))
        return response


class JobView(View):
    """
    View of a job

    - GET for a job state and properties
    - POST to re-submit a test by its test suite and related suts
    """
    def get(self, request, id):
        return JsonResponse(Job.objects.get(id=id).to_dict())

    def post(self, request, id):
        job = Job.objects.get(id=id)
        new_job = Job.objects.create(
                suite_reference=job.suite_reference,
                suite_content=job.suite_content,
                suts=job.suts,
                )
        response = JsonResponse({'id': new_job.id}, status=201)
        response['Location'] = urls_reverse('autotest:job', args=(new_job.id,))
        return response
