# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table(u'events_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('soundcloud_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('ignore_sc', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'events', ['Artist'])

        # Adding M2M table for field genres on 'Artist'
        m2m_table_name = db.shorten_name(u'events_artist_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm[u'events.artist'], null=False)),
            ('genre', models.ForeignKey(orm[u'events.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artist_id', 'genre_id'])

        # Adding model 'Genre'
        db.create_table(u'events_genre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('genre_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'events', ['Genre'])

        # Adding M2M table for field parent_id on 'Genre'
        m2m_table_name = db.shorten_name(u'events_genre_parent_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_genre', models.ForeignKey(orm[u'events.genre'], null=False)),
            ('to_genre', models.ForeignKey(orm[u'events.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_genre_id', 'to_genre_id'])

        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('event_date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Location'])),
            ('gay', self.gf('django.db.models.fields.BooleanField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field artists on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_artists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('artist', models.ForeignKey(orm[u'events.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'artist_id'])

        # Adding model 'Location'
        db.create_table(u'events_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('location_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('postal_code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country_code', self.gf('django.db.models.fields.CharField')(default='DE', max_length=2)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('fb_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'events', ['Location'])

        # Adding model 'ArtistNames'
        db.create_table(u'events_artistnames', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Artist'])),
        ))
        db.send_create_signal(u'events', ['ArtistNames'])

        # Adding model 'unkownGenre'
        db.create_table(u'events_unkowngenre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('soundcloud_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'events', ['unkownGenre'])


    def backwards(self, orm):
        # Deleting model 'Artist'
        db.delete_table(u'events_artist')

        # Removing M2M table for field genres on 'Artist'
        db.delete_table(db.shorten_name(u'events_artist_genres'))

        # Deleting model 'Genre'
        db.delete_table(u'events_genre')

        # Removing M2M table for field parent_id on 'Genre'
        db.delete_table(db.shorten_name(u'events_genre_parent_id'))

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field artists on 'Event'
        db.delete_table(db.shorten_name(u'events_event_artists'))

        # Deleting model 'Location'
        db.delete_table(u'events_location')

        # Deleting model 'ArtistNames'
        db.delete_table(u'events_artistnames')

        # Deleting model 'unkownGenre'
        db.delete_table(u'events_unkowngenre')


    models = {
        u'events.artist': {
            'Meta': {'object_name': 'Artist'},
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['events.Genre']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_sc': ('django.db.models.fields.BooleanField', [], {}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'soundcloud_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'})
        },
        u'events.artistnames': {
            'Meta': {'object_name': 'ArtistNames'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Artist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Artist']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'event_date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'gay': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Location']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {})
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
            'fb_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'events.unkowngenre': {
            'Meta': {'object_name': 'unkownGenre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'soundcloud_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['events']