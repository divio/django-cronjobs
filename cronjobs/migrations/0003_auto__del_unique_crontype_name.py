# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'CronType', fields ['name']
        db.delete_unique('cronjobs_crontype', ['name'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'CronType', fields ['name']
        db.create_unique('cronjobs_crontype', ['name'])


    models = {
        'cronjobs.cron': {
            'Meta': {'object_name': 'Cron'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 6, 7, 15, 34, 17, 602268)'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cronjobs.CronType']"})
        },
        'cronjobs.cronlog': {
            'Meta': {'object_name': 'CronLog'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
