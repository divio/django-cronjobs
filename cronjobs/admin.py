from django.contrib import admin
from cronjobs.models import CronLog

class CronLogAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', 'app_label', 'name', 'success', 'exception_message', 'duration',)
    list_display = ('timestamp', 'app_label', 'name', 'success',)
    list_filter = ('app_label', 'name', 'success',)
    
    def has_add_permission(self, *args, **kwargs):
        return False
    has_delete_permission = has_add_permission
    
admin.site.register(CronLog, CronLogAdmin)