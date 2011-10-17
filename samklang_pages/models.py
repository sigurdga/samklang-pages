from django.utils import simplejson

from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from s7n_utils import markdown

class Page(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    name = models.CharField(_('Name'), max_length=50)
    content = models.TextField(_('Content'), blank=True)
    content_html = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    group = models.ForeignKey(Group, related_name='pages', verbose_name=_('Group'), null=True, blank=True)
    admingroup = models.ForeignKey(Group, related_name='administers_pages', verbose_name=_('Writable for'))
    #document_class = models.SlugField(max_length=20, blank=True)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url',)
        db_table = 'samklang_page'
	app_label = 'Samklang'

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.name)

    @models.permalink
    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content.strip())
        super(Page, self).save(*args, **kwargs)

class PageWidget(models.Model):
    page = models.ForeignKey(Page, verbose_name=_('Page'), related_name='widgets')
    widget_name = models.CharField(max_length=30)
    position = models.IntegerField(verbose_name=_('Position'))
    options = models.TextField(blank=True, verbose_name=_('Options'))

    class Meta:
        verbose_name = _('Page widget')
        verbose_name_plural = _('Page widgets')
        ordering = ('position', 'widget_name')
	db_table = 'samklang_pagewidget'
	app_label = 'Samklang'

    def __unicode__(self):
        return u"%s: %s" % (self.widget_name, self.page.name)

    def widget(self):
        app, widget_name = self.widget_name.rsplit(".", 1)
        imp = __import__(app + ".pagewidgets", globals(), locals(), [widget_name])
        widget_class = getattr(imp, widget_name)
        try:
            options = simplejson.loads(self.options)
        except simplejson.JSONDecodeError:
            options = {}
        widget = widget_class(options)
        return widget
