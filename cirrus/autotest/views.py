from django.views import View

from django.http import JsonResponse  #, HttpResponse, StreamingHttpResponse


class SuiteIndexView(View):
    """
    get list, get query some, post new
    """
    def get(self, request):
        return JsonResponse({})

    def post(self, request):
        return JsonResponse({})


class SuiteDetailView(View):
    """
    get detail, delete, put to edit
    """
    def get(self, request):
        return JsonResponse({})

    def put(self, request):
        return JsonResponse({})

    def delete(self, request):
        return JsonResponse({})


class TaskIndexView(View):
    """
    get list, get query some, post to execute suite with suts
    """
    def get(self, request):
        return JsonResponse({})

    def post(self, request):
        return JsonResponse({})


class TaskDetailView(View):
    """
    get state and report, delete, post to re-execute its test data and variables
    """
    def get(self, request):
        return JsonResponse({})

    def post(self, request):
        return JsonResponse({})

    def delete(self, request):
        return JsonResponse({})
