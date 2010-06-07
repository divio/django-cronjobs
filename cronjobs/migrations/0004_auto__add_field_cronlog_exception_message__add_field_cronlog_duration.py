# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CronLog.exception_message'
        db.add_column('cronjobs_cronlog', 'exception_message', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'CronLog.duration'
        db.add_column('cronjobs_cronlog', 'duration', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=3), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CronLog.exception_message'
        db.delete_column('cronjobs_cronlog', 'exception_message')

        # Deleting field 'CronLog.duration'
        db.delete_column('cronjobs_cronlog', 'duration')


    models = {
        'cronjobs.cron': {
            'Meta': {'object_name': 'Cron'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 6, 7, 15, 42, 29, 846310)'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cronjobs.CronType']"})
        },
        'cronjobs.cronlog': {
            'Meta': {'object_name': 'CronLog'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '3'}),
            'exception_message': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'cronjobs.crontype': {
            'Meta': {'object_name': 'CronType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cache_timeout': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'run_every': ('django.db.models.fields.IntegerField', [], {'default': '86400'})
        }
    }

    complete_apps = ['cronjobs']
