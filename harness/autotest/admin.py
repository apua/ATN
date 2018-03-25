from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import TestData, TestExecution, Sut, Taas
from .tasks import execute_test


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'suite_name', 'suts', 'author')
    actions = ('execute',)

    def suts(self, td):
        suts_list = ''.join(f'<li>{s.info.splitlines()[0]}</li>' for s in td.sut.all())
        return mark_safe(f'<ul>{suts_list}</ul>')

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
            time.sleep(1)
            te = TestExecution.objects.get(pk=rq_job.id)
            if te:
                link = f'<a href="/admin/autotest/testexecution/{rq_job.id}">{te.start}</a>'
                self.message_user(request, mark_safe(f'Start test execution at: {link}'))
                break
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
    list_display = ('uuid', 'info', 'reserved_by', 'maintained_by')

    def save_model(self, request, sut, form, change):
        taas = Taas.objects.first()
        if taas is not None:
            import requests
            resp = requests.put(
                    f'http://{taas.ip}:{taas.port}/sut/{sut.uuid}',
                    json={
                        'info': sut.info,
                        'harness': {
                            'ip': settings.IP,
                            'port': settings.PORT,
                            },
                        'reserved_by': sut.reserved_by and sut.reserved_by.email,
                        'maintained_by': sut.maintained_by and sut.maintained_by.email,
                        },
                    )
            resp.raise_for_status()
        super().save_model(request, sut, form, change)


@admin.register(Taas)
class T(admin.ModelAdmin):
    list_display = ('ip', 'port')
