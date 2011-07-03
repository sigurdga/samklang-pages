from django.contrib import admin
from s7n.pages.models import Page, PageWidget
from s7n.pages.forms import PageForm

class PageAdminForm(PageForm):

    class Meta:
        fields = ('url', 'name', 'content', 'site', 'user', 'group', 'admingroup', 'document_class')

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('url', 'name')
    search_fields = ('url', 'name')

admin.site.register(Page, PageAdmin)

class PageWidgetAdmin(admin.ModelAdmin):
    pass

admin.site.register(PageWidget, PageWidgetAdmin)

