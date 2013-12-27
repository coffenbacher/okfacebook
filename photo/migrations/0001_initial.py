# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photo'
        db.create_table(u'photo_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photos', null=True, to=orm['facebook.FacebookProfile'])),
            ('okcupid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photos', null=True, to=orm['okcupid.OkCupidProfile'])),
            ('_ahash', self.gf('django.db.models.fields.TextField')(db_column='ahash')),
            ('_phash', self.gf('django.db.models.fields.TextField')(db_column='phash')),
            ('_dhash', self.gf('django.db.models.fields.TextField')(db_column='dhash')),
        ))
        db.send_create_signal(u'photo', ['Photo'])

        # Adding model 'PhotoMatch'
        db.create_table(u'photo_photomatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('a_dist', self.gf('django.db.models.fields.FloatField')()),
            ('p_dist', self.gf('django.db.models.fields.FloatField')()),
            ('d_dist', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'photo', ['PhotoMatch'])

        # Adding M2M table for field photos on 'PhotoMatch'
        m2m_table_name = db.shorten_name(u'photo_photomatch_photos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photomatch', models.ForeignKey(orm[u'photo.photomatch'], null=False)),
            ('photo', models.ForeignKey(orm[u'photo.photo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photomatch_id', 'photo_id'])


    def backwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table(u'photo_photo')

        # Deleting model 'PhotoMatch'
        db.delete_table(u'photo_photomatch')

        # Removing M2M table for field photos on 'PhotoMatch'
        db.delete_table(db.shorten_name(u'photo_photomatch_photos'))


    models = {
        u'facebook.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'fbid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.Spider']"})
        },
        u'okcupid.okcupidprofile': {
            'Meta': {'object_name': 'OkCupidProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'okid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spider.Spider']"})
        },
        u'photo.photo': {
            'Meta': {'object_name': 'Photo'},
            '_ahash': ('django.db.models.fields.TextField', [], {'db_column': "'ahash'"}),
            '_dhash': ('django.db.models.fields.TextField', [], {'db_column': "'dhash'"}),
            '_phash': ('django.db.models.fields.TextField', [], {'db_column': "'phash'"}),
            'facebook': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': u"orm['facebook.FacebookProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'okcupid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': u"orm['okcupid.OkCupidProfile']"})
        },
        u'photo.photomatch': {
            'Meta': {'object_name': 'PhotoMatch'},
            'a_dist': ('django.db.models.fields.FloatField', [], {}),
            'd_dist': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_dist': ('django.db.models.fields.FloatField', [], {}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['photo.Photo']", 'symmetrical': 'False'})
        },
        u'spider.spider': {
            'Meta': {'object_name': 'Spider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['photo']