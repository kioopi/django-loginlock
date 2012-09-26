# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'LoginCandidate.timestamp'
        db.delete_column('loginlock_logincandidate', 'timestamp')

        # Adding field 'LoginCandidate.last_attempt_at'
        db.add_column('loginlock_logincandidate', 'last_attempt_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(1980, 5, 13), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'LoginCandidate.timestamp'
        db.add_column('loginlock_logincandidate', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(1980, 5, 13), blank=True), keep_default=False)

        # Deleting field 'LoginCandidate.last_attempt_at'
        db.delete_column('loginlock_logincandidate', 'last_attempt_at')


    models = {
        'loginlock.logincandidate': {
            'Meta': {'ordering': "['-last_attempt_at']", 'unique_together': "(('username', 'ip_address'),)", 'object_name': 'LoginCandidate'},
            'attempt_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'last_attempt_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['loginlock']
