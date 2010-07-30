from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta


class CronTypeManager(models.Manager):
    def for_class(self, cron_class):
        obj, created = self.get_or_create(
            app_label = cron_class.__module__.split('.')[-2],
            name = cron_class.__name__,
        )
        if created or cron_class.run_every != obj.run_every:
            obj.run_every = cron_class.run_every
            obj.save()
        return obj


class CronType(models.Model):
    app_label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    run_every = models.IntegerField(default=86400)
    cache_timeout = models.PositiveIntegerField(default=0)
    
    objects = CronTypeManager()

    def __unicode__(self):
        return u'%s.%s' % (self.app_label, self.name)


class Cron(models.Model):
    type = models.ForeignKey(CronType)
    next_run = models.DateTimeField(default=datetime.now())

    def run(self):
        self.next_run = datetime.now() + timedelta(seconds=self.type.run_every)
        self.save()

    class Meta:
        pass
    
class CronLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    app_label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    success = models.BooleanField()
    exception_message = models.TextField(default="")
    duration = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __unicode__(self):
        return '%s.%s: %s' % (self.app_label, self.name, 'OK' if self.success else 'FAILED')