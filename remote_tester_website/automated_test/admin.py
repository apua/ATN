from django.contrib import admin
from django.apps import apps


for name, model in apps.get_app_config('automated_test').models.items():
    admin.site.register(model)
