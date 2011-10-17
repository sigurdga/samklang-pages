from django.contrib import admin
from samklang_pages.models import Page, PageWidget
from samklang_pages.forms import PageForm

class PageWidgetInline(admin.TabularInline):
    model = PageWidget

class PageAdminForm(PageForm):

    class Meta:
        fields = ('url', 'name', 'content', 'site', 'user', 'group', 'admingroup',)# 'document_class')

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('url', 'name')
    search_fields = ('url', 'name')
    inlines = [
        PageWidgetInline,
    ]

admin.site.register(Page, PageAdmin)

class PageWidgetAdmin(admin.ModelAdmin):
    pass

admin.site.register(PageWidget, PageWidgetAdmin)

