# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CronLog'
        db.create_table('cronjobs_cronlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('cronjobs', ['CronLog'])


    def backwards(self, orm):
        
        # Deleting model 'CronLog'
        db.delete_table('cronjobs_cronlog')


    models = {
        'cronjobs.cron': {
            'Meta': {'object_name': 'Cron'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 6, 7, 15, 15, 17, 846583)'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'run_every': ('django.db.models.fields.IntegerField', [], {'default': '86400'})
        }
    }

    complete_apps = ['cronjobs']
