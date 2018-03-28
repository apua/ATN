from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import TestData, TestExecution, Sut, Taas, TestResult


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'related_suts', 'author')
    actions = ('execute',)

    def related_suts(self, td):
        suts_list = ''.join(f'<li>{s.name}</li>' for s in td.suts.all())
        return mark_safe(f'<ul>{suts_list}</ul>')

    def execute(self, request, queryset):
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

        rq_job = td.submit_test_execution()

        timeout = 3
        for _ in range(timeout):
            time.sleep(1)
            te = TestExecution.objects.get(pk=rq_job.id)
            if te:
                link = f'<a href="/admin/autotest/testexecution/{rq_job.id}/">{te.start}</a>'
                self.message_user(request, mark_safe(f'Start test execution at: {link}'))
                break
        else:
            self.message_user(request, 'Unknown error to execute test', level=messages.ERROR)


@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('start', 'console', 'report')
    list_display_links = None
    ordering = ('-start',)

    def report(self, te):
        if te.test_result:
            return mark_safe(f'<a href="/test-reporting/{te.pk}/report.html">report</a>')

    def console(self, te):
        html_id = f'te-id-{te.rq_jid.hex}'
        xhr = f'xhr{te.rq_jid.hex}'
        trs = TestResult.objects.filter(test_execution=te)
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


@admin.register(Sut)
class SutAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'info', 'reserved_by', 'in_use')

    def save_model(self, request, sut, form, change):
        taas = Taas.objects.first()
        if taas is not None:
            import requests
            resp = requests.put(
                    f'http://{taas}/sut/{sut.uuid}/',
                    json=sut.to_dict(),
                    )
            resp.raise_for_status()
        super().save_model(request, sut, form, change)
