import requests

from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import ExecLayer, Sut, TestData, TestExecution, TestResult


local_site = 'http://127.0.0.1:8000'


@admin.register(ExecLayer)
class E(admin.ModelAdmin):
    list_display = ('id', 'ip', 'port')


@admin.register(Sut)
class S(admin.ModelAdmin):
    list_display = ('uuid', 'exec_layer', 'reserved_by', 'maintained_by')

    def save_model(self, request, sut, form, change):
        resp = requests.put(
                f'http://{sut.exec_layer.ip}:{sut.exec_layer.port}/sut/{sut.uuid}',
                json={
                    'reserved_by': sut.reserved_by and sut.reserved_by.email,
                    'maintained_by': sut.maintained_by and sut.maintained_by.email,
                    },
                )
        resp.raise_for_status()
        super().save_model(request, sut, form, change)


@admin.register(TestData)
class T(admin.ModelAdmin):
    actions = ('execute',)

    def execute(self, request, queryset):
        import json
        import time

        if len(queryset) != 1:
            self.message_user(request, 'Please select just one to execute', level=messages.ERROR)
            return

        td = queryset[0]
        source = json.loads(td.test_data)
        te = TestExecution.objects.create(test_data=td, origin=td.test_data)
        r = requests.post(
                f'{local_site}/execute_test/',
                json={"test_data": source, "remote_id": te.id},
                )
        r.raise_for_status()
        print(r.json())
        te.rq_jid = r.json()['rq_jid']
        te.save(update_fields=['rq_jid'])


@admin.register(TestExecution)
class Te(admin.ModelAdmin):
    actions = None
    list_display = ('id', 'rq_jid', 'start', 'console', 'origin')

    def console(self, te):
        html_id = f'te-id-{te.id}'
        xhr = f'xhr{te.id}'
        trs = TestResult.objects.filter(test_execution=te)
        if trs:
            return mark_safe(f'<pre id="{html_id}">{trs.first().console}</pre>')
        else:
            return mark_safe(f'''
                    <pre id="{html_id}"></pre>
                    <script>
                    var {xhr} = new XMLHttpRequest();
                    {xhr}.open("GET", "/testexecution/{te.rq_jid}", true);
                    {xhr}.onreadystatechange = function() {{
                        var s = document.querySelector("#{html_id}");
                        if({xhr}.readyState === XMLHttpRequest.LOADING) {{
                            s.textContent = {xhr}.responseText;
                        }}
                    }};
                    {xhr}.send();
                    </script>
                    ''')


admin.site.register(TestResult)
