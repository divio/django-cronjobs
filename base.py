
from django.utils.safestring import SafeUnicode

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

        if 'run_every' not in attrs:
            attrs['run_every'] = 86400
        else:
            attrs['run_every'] *= 3600

        # Create the class.
        module = type.__new__(cls, name, bases, attrs)
        from cronjobs import loading
        # Register the class for future reference
        loading.registry.register(name, module)

        return module

class Cron(object):
    __metaclass__ = CronBase
    run_every = 86400

    def __init__(self, id='', **kwargs):
        self.id = id
        from cronjobs import models
        cron_type = models.CronType.for_class(self.__class__)
        self._record = models.Cron.objects.get_or_create(type=cron_type)[0]
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
