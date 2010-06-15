from cronjobs.base import CronFailed, SkipJob
from cronjobs.models import CronLog
from datetime import datetime
from django.conf import settings
import os
import time
import traceback

def _format_exception(e):
    if isinstance(e, CronFailed):
        return "CronFailed: %s" % e.message
    return traceback.format_exc()

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

        ret = {'cron_jobs':{'run':0, 'succeeded':0, 'locked': 0}}
        now = datetime.now()
        for c in crons:
            cron = c()
            if cron.next_run <= now:
                if not cron.lock.is_active:
                    success = False
                    exception_message = ""
                    duration = 0.0
                    try:
                        ret['cron_jobs']['run'] += 1                        
                        start = time.time()
                        try:
                            status = cron.job()
                            status = status or status is None
                        except CronFailed, e:
                            status = False
                            exception_message = _format_exception(e)
                        except SkipJob, e:
                            continue
                        stop = time.time()
                        duration = stop - start
                        if status:
                            cron._record.run()
                            ret['cron_jobs']['succeeded'] += 1
                            success = True
                        else:
                            exception_message = "Job returned: %s" % status
                    except Exception, e:
                        exception_message = _format_exception(e)
                        raise
                    finally:
                        CronLog.objects.create(
                            app_label=cron._record.type.app_label,
                            name=cron._record.type.name,
                            success=success,
                            duration=str(duration),
                            exception_message=exception_message,
                        )
                else:
                    ret['cron_jobs']['locked'] += 1
        return ret

registry = CronCache()
