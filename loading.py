from django.conf import settings
from datetime import datetime

class CronCache(object):
    def __init__(self):
        self.discovered = False
        self.crons = {}

    def register(self, name, module):
        """
        Register the cron in cache for later use.
        """
        if name in self.crons:
            raise KeyError, "Only one cron named %s can be registered." % name

        self.crons[name] = module

    def discover_crons(self):
        if self.discovered:
            return
        for app in settings.INSTALLED_APPS:
            # Just loading the module will do the trick
            __import__(app, {}, {}, ['cron'])
        self.discovered = True

    def get_all_crons(self):
        self.discover_crons()
        return self.crons.values()
    
    def run(self):
        """
        Return a list of cron instances that are valid.
        """
        crons = self.get_all_crons()

        ret = {'cron_jobs':{'run':0, 'succeeded':0}}
        for c in crons:
            cron = c()
            if cron.next_run <= datetime.now() and cron.job():
                cron._record.run()
                ret['cron_jobs']['succeeded'] += 1
            ret['cron_jobs']['run'] += 1
        return ret

registry = CronCache()
