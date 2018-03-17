from django.contrib import admin

from .models import ExecLayer, Sut, TestData, TestExecution, TestResult


@admin.register(ExecLayer)
class E(admin.ModelAdmin):
    list_display = ('id', 'ip')


@admin.register(Sut)
class S(admin.ModelAdmin):
    list_display = ('uuid', 'exec_layer', 'reserved_by', 'maintained_by')


admin.site.register(TestData)
admin.site.register(TestExecution)
admin.site.register(TestResult)
