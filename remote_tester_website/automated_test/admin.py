from django.contrib import admin

from .models import (Harness, Sut, Reservation,
                     TestData, TestExecution)


@admin.register(Harness)
class HarnessAdmin(admin.ModelAdmin):
    list_display = ('ip',)

@admin.register(Sut)
class SutAdmin(admin.ModelAdmin):
    list_display = ('oobm', 'harness')

@admin.register(Reservation)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('sut', 'user', 'start_time', 'end_time')

admin.site.register(TestData)
admin.site.register(TestExecution)
