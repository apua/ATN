import requests

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import TestHarness, Sut, TestData, TestExecution, TestResult


#local_site = 'http://127.0.0.1:2345'
local_site = NotImplemented


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
        3.  Mark the test harness as registered
        4.  Add test harness and SUTs
        """
        taas = requests.get(f'http://{th.ip}:{th.port}/taas/').json()
        if taas:
            raise Exception(f'Test harness {th.ip}:{th.port} is registered on'
                            f' TaaS {taas["ip"]}:{taas["port"]} already')

        requests.put(
                f'http://{th.ip}:{th.port}/taas/',
                json={
                    'ip': settings.IP,
                    'port': settings.PORT,
                    },
                ).raise_for_status()
        suts = requests.get(f'http://{th.ip}:{th.port}/sut/').json()

        super().save_model(request, th, form, change)

        Sut.load_all(th, suts)

    def delete_model(self, request, th):
        """
        Unregister a test harness from TaaS itself

        1.  Verify the test harness is registered by TaaS itself
        2.  Remove test harness and SUTs
        3.  Mark the test harness not registered
        """
        taas = requests.get(f'http://{th.ip}:{th.port}/taas/').json()
        if not taas or taas != {'ip': settings.IP, 'port': settings.PORT}:
            raise Exception(f'Test harness {th.ip}:{th.port} is not'
                            f' register on TaaS {settings.IP}:{settings.PORT} yet')

        super().delete_model(request, th)

        requests.put(f'http://{th.ip}:{th.port}/taas/', json={}).raise_for_status()


@admin.register(Sut)
class S(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'harness', 'reserved_by', 'in_use')

    def save_model(self, request, sut, form, change):
        resp = requests.post(
                f'http://{sut.harness}/sut/{sut.uuid}/reserve/',
                json={'reserved_by': sut.reserved_by and sut.reserved_by.email},
                )
        resp.raise_for_status()
        resp = requests.post(
                f'http://{sut.harness}/sut/{sut.uuid}/use/',
                json={'in_use': sut.in_use},
                )
        resp.raise_for_status()
        super().save_model(request, sut, form, change)


@admin.register(TestData)
class T(admin.ModelAdmin):
    list_display = ('id', 'related_suts', 'author')
    actions = ('execute',)

    def related_suts(self, td):
        suts_list = ''.join(f'<li>{s.name}</li>' for s in td.suts.all())
        return mark_safe(f'<ul>{suts_list}</ul>')

    def execute(self, request, queryset):
        import json
        import time

        if len(queryset) != 1:
            self.message_user(request, 'Please select just one to execute', level=messages.ERROR)
            return

        td = queryset[0]
        if not td.is_executable_by(request.user):
            mesg = (
                    f'You cannot execute the test data. Possible reasons:'
                    f' 1. You are not the author of the test data'
                    f' 2. Required SUTs are not all reserved by you'
                    f' 3. Required SUTs are in testing'
                    )
            self.message_user(request, mesg, level=messages.ERROR)
            return

        rq_jid = td.submit_test_execution()


@admin.register(TestExecution)
class Te(admin.ModelAdmin):
    actions = None
    list_display = ('id', 'rq_jid', 'start', 'console', 'report')

    def report(self, te):
        if te.test_result:
            return mark_safe(f'<a href="/test-reporting/{te.pk}/report.html">report</a>')

    def console(self, te):
        if te.rq_jid is None: print("te.rq_jid is None"); return  # TODO: remove it
        html_id = f'te-id-{te.id}'
        xhr = f'xhr{te.id}'
        trs = TestResult.objects.filter(test_execution=te)  # TODO: better way like `get`?
        if trs:
            return mark_safe(f'<pre id="{html_id}">{trs.first().console}</pre>')
        else:
            return mark_safe(f'''
                    <pre id="{html_id}"></pre>
                    <script>
                    var {xhr} = new XMLHttpRequest();
                    {xhr}.open("GET", "/test-execution/{te.rq_jid}/console/", true);
                    {xhr}.onreadystatechange = function() {{
                        var s = document.querySelector("#{html_id}");
                        if({xhr}.readyState === XMLHttpRequest.LOADING
                           || {xhr}.readyState === XMLHttpRequest.DONE) {{
                            s.textContent = {xhr}.responseText;
                        }}
                    }};
                    {xhr}.send();
                    </script>
                    ''')


admin.site.register(TestResult)
