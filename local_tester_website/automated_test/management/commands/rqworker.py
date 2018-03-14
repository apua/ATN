from django.core.management.base import BaseCommand
from redis import Redis
from rq import Worker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('queue_names', nargs='+')
        parser.add_argument('--test', action='store_true')

    def handle(self, queue_names, test, **options):
        from django.conf import settings

        if test:
            db_setting = settings.DATABASES['default']
            db_setting['NAME'] = db_setting['TEST']['NAME']

        Worker(queue_names, connection=Redis()).work()

