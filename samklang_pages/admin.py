from django.contrib import admin
from samklang_pages.models import Page
from samklang_pages.forms import PageForm

class PageAdminForm(PageForm):

    class Meta:
        fields = ('url', 'name', 'content', 'site', 'user', 'group', 'admingroup',)# 'document_class')

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('url', 'name')
    search_fields = ('url', 'name')

admin.site.register(Page, PageAdmin)
