import json

from django.contrib import admin, messages

from .models import TestData, TestExecution, TestResult
from .tasks import execute_test

from django.utils.safestring import mark_safe


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'suite_name', 'author')
    actions = ('execute',)

    def suite_name(self, td):
        return json.loads(td.test_data)['filename']

    def execute(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'Please select just one to execute', level=messages.ERROR)
            return

        td = queryset[0]
        source = json.loads(td.test_data)
        command = f'pybot {source["filename"]}'
        rq_job = execute_test.delay(cmd=command, td_src=source, td_id=td.id)


@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['start', 'tester', 'test_data']

    def tester(self, te):
        td = te.test_data
        return td and td.author


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    pass
