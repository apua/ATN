from celery import shared_task
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Suite, Result


@shared_task
def execute(suite_id: int, suite_content: str):
    """
    Execute test by single test suite in string.

    Use temporary file as a workaround, and only support log currently.
    """
    import os, tempfile

    from robot.api import TestSuiteBuilder, ResultWriter

    assert type(suite_id) is int and type(suite_content) is str

    with tempfile.NamedTemporaryFile(suffix='.robot', delete=False) as fp:
        fp.write(suite_content.encode())
    
    try:
        suite = TestSuiteBuilder().build(fp.name)
        result = suite.run(output=None, critical='rat')
        ResultWriter(result).write_results(report=None, log=fp.name)
    except robot.errors.DataError as e:
        import traceback
        Result(log_content=f'<pre>{ "".join(traceback.format_exc()) }</pre>',
               suite_content=suite_content,
               origin_suite_id=suite_id).save()
    else:
        Result(log_content=open(fp.name).read(),
               suite_content=suite_content,
               origin_suite_id=suite_id).save()
    finally:
        os.unlink(fp.name)


@admin.register(Suite)
class SuiteAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    actions = ('execute_suites',)

    def execute_suites(self, request, queryset):
        for suite in queryset:
            execute.delay(suite.id, suite.content)
    execute_suites.short_description = 'Execute selected suites'

    def get_action_choices(self, request):
        # NOTE: This is undocumented in Django
        choices = super().get_action_choices(request)
        return [(name, desc) for name, desc in choices[1:] if name != 'delete_selected']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('create_time', 'origin_suite')
    fields = readonly_fields = ('suite', 'log')

    def log(self, instance):
        return mark_safe(instance.log_content)

    def suite(self, instance):
        return instance.suite_content

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
