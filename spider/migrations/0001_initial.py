# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Spider'
        db.create_table(u'spider_spider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'spider', ['Spider'])

        # Adding model 'OkCupidAccount'
        db.create_table(u'spider_okcupidaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'spider', ['OkCupidAccount'])


    def backwards(self, orm):
        # Deleting model 'Spider'
        db.delete_table(u'spider_spider')

        # Deleting model 'OkCupidAccount'
        db.delete_table(u'spider_okcupidaccount')


    models = {
        u'spider.okcupidaccount': {
            'Meta': {'object_name': 'OkCupidAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'spider.spider': {
            'Meta': {'object_name': 'Spider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['spider']