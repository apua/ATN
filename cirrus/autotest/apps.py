from pathlib import Path

from django.apps import AppConfig


class AutotestConfig(AppConfig):
    name = 'autotest'
    verbose_name = 'Automated Test'
    workspace = Path('/tmp')
