from cronjobs.constants import DAYS, HOURS
from django.utils.safestring import SafeUnicode
import os
import time

def _job_decorator(func):
    def _wrapped(self):
        if not self.lock.is_active:
            self.lock.aquire()
            try:
                resp = func(self)
            finally:
                self.lock.release()
            return resp
        return False
    _wrapped.__name__ = func.__name__
    return _wrapped


class CronFailed(Exception): pass
class SkipJob(Exception): pass


class CronLock(object):
    def __init__(self, cls):
        self.cls = cls
        self.base_path = os.path.abspath(os.path.dirname(__import__(cls.__module__).__file__))
        self.filename = '.%s.lockfile' % cls.__class__.__name__
    
    def get_lock_path(self):
        return os.path.abspath(os.path.join(self.base_path, self.filename))
    
    @property
    def is_active(self):
        return os.path.exists(self.get_lock_path())
    
    def aquire(self):
        lockfile = open(self.get_lock_path(), 'w')
        lockfile.write(str(time.time()))
        lockfile.close()
        
    def age(self):
        if self.is_active:
            lockfile = open(self.get_lock_path(), 'r')
            timestamp = lockfile.read().strip()
            lockfile.close()
            return timet.time() - float(timestamp)
        return 0.0
    
    def release(self):
        try:
            os.remove(self.get_lock_path())
        except OSError:
            pass
        
    def __nonzero__(self):
        return int(self.is_active)
        
    def __repr__(self):
        return '<CronLock of %s: %s>' % (self.cls.__name__, bool(self))


class CronBase(type):
    def __new__(cls, name, bases, attrs):
        # If this isn't a subclass of Cron, don't do anything special.
        try:
            if not filter(lambda b: issubclass(b, Cron), bases):
                return super(CronBase, cls).__new__(cls, name, bases, attrs)
        except NameError:
            # 'Model' isn't defined yet, meaning we're looking at Django's own
            # Model class, defined below.
            return super(CronBase, cls).__new__(cls, name, bases, attrs)
        
        interval_unit = attrs.get('interval_unit', HOURS)
        
        if 'run_every' not in attrs:
            attrs['run_every'] = 1 * DAYS
        else:
            attrs['run_every'] *= interval_unit
            
        # decorate the job method
        
        attrs['job'] = _job_decorator(attrs['job'])

        # Create the class.
        klass = type.__new__(cls, name, bases, attrs)
        klass.lock = CronLock(klass)
        from cronjobs import loading
        # Register the class for future reference
        loading.registry.register(name, klass)

        return klass


class Cron(object):
    __metaclass__ = CronBase
    run_every = 1
    interval_unit = DAYS

    def __init__(self, id='', **kwargs):
        self.id = id
        from cronjobs.models import CronType, Cron
        cron_type = CronType.objects.for_class(self.__class__)
        self._record = Cron.objects.get_or_create(type=cron_type)[0]
        self.type = cron_type
    
    def job(self):
        """
        The Job to Execute
        """
        return False

    def get_next_run(self):
        return self._record.next_run
    next_run = property(get_next_run)

    def __unicode__(self):
        return SafeUnicode(unicode(self.render()))