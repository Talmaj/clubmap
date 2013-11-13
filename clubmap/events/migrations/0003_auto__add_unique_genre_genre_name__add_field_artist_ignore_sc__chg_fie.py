# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Genre', fields ['genre_name']
        db.create_unique(u'events_genre', ['genre_name'])

        # Adding field 'Artist.ignore_sc'
        db.add_column(u'events_artist', 'ignore_sc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Artist.soundcloud_id'
        db.alter_column(u'events_artist', 'soundcloud_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Genre', fields ['genre_name']
        db.delete_unique(u'events_genre', ['genre_name'])

        # Deleting field 'Artist.ignore_sc'
        db.delete_column(u'events_artist', 'ignore_sc')


        # Changing field 'Artist.soundcloud_id'
        db.alter_column(u'events_artist', 'soundcloud_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

    models = {
        u'events.artist': {
            'Meta': {'object_name': 'Artist'},
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['events.Genre']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_sc': ('django.db.models.fields.BooleanField', [], {}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'soundcloud_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'events.artistnames': {
            'Meta': {'object_name': 'ArtistNames'},
            'artist': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Artist']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Artist']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event_date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'event_date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Location']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'events.genre': {
            'Meta': {'object_name': 'Genre'},
            'genre_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parent_id_rel_+'", 'to': u"orm['events.Genre']"})
        },
        u'events.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country_code': ('django.db.models.fields.CharField', [], {'default': "'DE'", 'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'postal_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['events']