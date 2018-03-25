import requests

from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import TestHarness, Sut, TestData, TestExecution, TestResult


#local_site = 'http://127.0.0.1:2345'
#taas_self = {'ip': '127.0.0.1', 'port': 1234}
local_site = NotImplemented
taas_self = NotImplemented


@admin.register(TestHarness)
class H(admin.ModelAdmin):
    list_display = ('ip_port',)
    actions = None

    def ip_port(self, inst):
        return f'{inst.ip}:{inst.port}'

    def save_model(self, request, th, form, change):
        """
        Register a test harness onto TaaS itself

        1.  Verify the test harness is not registered yet
        2.  Fetch all SUTs from the test harness
        3.  Label the test harness as registered
        """
        taas = requests.get(f'http://{th.ip}:{th.port}/taas/').json()
        if taas:
            raise Exception(f'Test harness {th.ip}:{th.port} is registered on'
                            f' TaaS {taas["ip"]}:{taas["port"]} already')

        requests.put(
                f'http://{th.ip}:{th.port}/taas/',
                json=taas_self,
                ).raise_for_status()
        suts = requests.get(f'http://{th.ip}:{th.port}/sut/').json()

        super().save_model(request, th, form, change)

        Sut.load_all(th, suts)

    def delete_model(self, request, th):
        """
        Unregister a test harness from TaaS itself

        1.  Verify the test harness is registered by TaaS itself
        2.  Remove test harness and SUTs
        3.  Label the test harness not registered
        """
        taas = requests.get(f'http://{th.ip}:{th.port}/taas/').json()
        if not taas or taas != taas_self:
            raise Exception(f'Test harness {th.ip}:{th.port} is not'
                            f' register on TaaS {taas_self["ip"]}:{taas_self["port"]} yet')

        requests.put(f'http://{th.ip}:{th.port}/taas/', json={}).raise_for_status()

        super().delete_model(request, th)


@admin.register(Sut)
class S(admin.ModelAdmin):
    list_display = ('uuid', 'harness', 'reserved_by', 'maintained_by')

    def save_model(self, request, sut, form, change):
        resp = requests.put(
                f'http://{sut.harness.ip}:{sut.harness.port}/sut/{sut.uuid}',
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
