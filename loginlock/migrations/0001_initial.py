# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'LoginCandidate'
        db.create_table('loginlock_logincandidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
            ('attempt_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('loginlock', ['LoginCandidate'])

        # Adding unique constraint on 'LoginCandidate', fields ['username', 'ip_address']
        db.create_unique('loginlock_logincandidate', ['username', 'ip_address'])


    def backwards(self, orm):

        # Removing unique constraint on 'LoginCandidate', fields ['username', 'ip_address']
        db.delete_unique('loginlock_logincandidate', ['username', 'ip_address'])

        # Deleting model 'LoginCandidate'
        db.delete_table('loginlock_logincandidate')


    models = {
        'loginlock.logincandidate': {
            'Meta': {'ordering': "['-timestamp']", 'unique_together': "(('username', 'ip_address'),)", 'object_name': 'LoginCandidate'},
            'attempt_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['loginlock']
