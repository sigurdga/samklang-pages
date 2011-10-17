# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('samklang_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pages', null=True, to=orm['auth.Group'])),
            ('admingroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='administers_pages', to=orm['auth.Group'])),
        ))
        db.send_create_signal('samklang_pages', ['Page'])

        # Adding model 'PageWidget'
        db.create_table('samklang_pagewidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='widgets', to=orm['samklang_pages.Page'])),
            ('widget_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('options', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('samklang_pages', ['PageWidget'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('samklang_page')

        # Deleting model 'PageWidget'
        db.delete_table('samklang_pagewidget')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'samklang_pages.page': {
            'Meta': {'ordering': "('url',)", 'object_name': 'Page', 'db_table': "'samklang_page'"},
            'admingroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'administers_pages'", 'to': "orm['auth.Group']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'samklang_pages.pagewidget': {
            'Meta': {'ordering': "('position', 'widget_name')", 'object_name': 'PageWidget', 'db_table': "'samklang_pagewidget'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widgets'", 'to': "orm['samklang_pages.Page']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'widget_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['samklang_pages']
