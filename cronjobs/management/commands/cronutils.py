#
# run the cron service (intended to be executed from a cron job)
#
# usage: manage.py cronjobs

from django.core.management.base import BaseCommand
from cronjobs.loading import registry

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-c", "--crons",
            dest="action",
            action="store_const",
            const="crons",
            help='Show all crons'),
        make_option("-l", "--locks",
            dest="action",
            action="store_const",
            const="locks",
            help='Show active locks'),
        make_option("-u", "--unlock",
            dest="action",
            action="store_const",
            const="unlock",
            help='Unlock specified locks'),
        )

    def handle(self, *args, **options):
        registry.discover_crons()
        action = options.get('action', 'crons')
        getattr(self, 'handle_%s' % action)()
            
    def get_locks(self):
        for cron in registry.get_all_crons():
            if cron.lock.is_active:
                yield lock
                
    def handle_crons(self):
        print "Available crons:"
        for cron in [c() for c in registry.crons.values()]:
            next = cron._record.next_run
            locked = cron.lock.is_active
            name = unicode(cron)
            print ' %s (next run: %s, locked: %s)' % (name, next, 'True' if locked else 'False')
        print
            
    def handle_locks(self):
        from cronjobs.loading import registry
        print "Currently active cron locks:"
        for lock in self.get_locks():
            print " %s (%s seconds old)" % (cron, cron.lock.age)
        print
                
    def handle_unlock(self, *names):
        print "Unlocking crons"
        for name in names:
            cron = registry.crons.get(name)
            if cron and cron.lock.is_active:
                cron.lock.release()
                print " Released lock of %s" % cron
            else:
                print " Cron '%s' not found or not locked" % name