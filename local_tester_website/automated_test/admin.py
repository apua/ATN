from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import TestData, TestExecution, Sut
from .tasks import execute_test


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'suite_name', 'author')
    actions = ('execute',)

    def suite_name(self, td):
        import json

        return json.loads(td.test_data)['filename']

    def execute(self, request, queryset):
        import json
        import time

        if len(queryset) != 1:
            self.message_user(request, 'Please select just one to execute', level=messages.ERROR)
            return

        td = queryset[0]
        source = json.loads(td.test_data)
        command = f'pybot {source["filename"]}'
        rq_job = execute_test.delay(cmd=command, td_src=source, td_id=td.id)

        timeout = 3
        for _ in range(timeout):
            te = TestExecution.objects.get(pk=rq_job.id)
            if te:
                link = f'<a href="/admin/automated_test/testexecution/{rq_job.id}">{te.start}</a>'
                self.message_user(request, mark_safe(f'Start test execution at: {link}'))
                break
            time.sleep(1)
        else:
            self.message_user(request, 'Unknown error to execute test', level=messages.ERROR)


@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('start', 'console', 'origin')
    list_display_links = None

    def console(self, te):
        if te.test_result:
            c = te.test_result.console
        else:
            consoles = ConsoleLine.objects.filter(test_execution=te).order_by('id')
            c = ''.join(c.output for c in consoles)
        return mark_safe(f'<pre>{c}</pre>')


@admin.register(Sut)
class SutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'credential', 'reserved_by', 'maintained_by')
