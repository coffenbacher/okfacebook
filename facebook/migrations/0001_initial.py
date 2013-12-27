# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacebookProfile'
        db.create_table(u'facebook_facebookprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fbid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spider.Spider'])),
            ('scraped', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'facebook', ['FacebookProfile'])


    def backwards(self, orm):
        # Deleting model 'FacebookProfile'
        db.delete_table(u'facebook_facebookprofile')


    models = {
        u'facebook.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'fbid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.Spider']"})
        },
        u'spider.spider': {
            'Meta': {'object_name': 'Spider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['facebook']