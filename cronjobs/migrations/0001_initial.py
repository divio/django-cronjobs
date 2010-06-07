# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CronType'
        db.create_table('cronjobs_crontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('run_every', self.gf('django.db.models.fields.IntegerField')(default=86400)),
            ('cache_timeout', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('cronjobs', ['CronType'])

        # Adding model 'Cron'
        db.create_table('cronjobs_cron', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cronjobs.CronType'])),
            ('next_run', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 6, 7, 15, 13, 18, 37377))),
        ))
        db.send_create_signal('cronjobs', ['Cron'])


    def backwards(self, orm):
        
        # Deleting model 'CronType'
        db.delete_table('cronjobs_crontype')

        # Deleting model 'Cron'
        db.delete_table('cronjobs_cron')


    models = {
        'cronjobs.cron': {
            'Meta': {'object_name': 'Cron'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 6, 7, 15, 13, 18, 37377)'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cronjobs.CronType']"})
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
