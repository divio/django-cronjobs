#
# run the cron service (intended to be executed from a cron job)
#
# usage: manage.py cronjobs

from django.core.management.base import BaseCommand
from cronjobs.loading import registry

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "run the cron services (intended to be executed from a cron job)"
    
    def handle(self, **options):
        result = registry.run()
        return "all cronjobs finished successfully. checked %d jobs, actually run %d" % (result['cron_jobs']['run'], result['cron_jobs']['succeeded'])
