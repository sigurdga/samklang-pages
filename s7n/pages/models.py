from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from s7n.utils import markdown

class Page(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    name = models.CharField(_('Name'), max_length=50)
    content = models.TextField(_('Content'), blank=True)
    content_html = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    group = models.ForeignKey(Group, related_name='pages', verbose_name=_('Group'), null=True, blank=True)
    admingroup = models.ForeignKey(Group, related_name='administers_pages', verbose_name=_('Writable for'))

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url',)
        db_table = 's7n_page'

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.name)

    @models.permalink
    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content)
        super(Page, self).save(*args, **kwargs)

