from django.contrib import admin
from s7n.pages.models import Page
from s7n.pages.forms import PageForm

class PageAdminForm(PageForm):

    class Meta:
        fields = ('url', 'name', 'content', 'sites', 'user', 'group', 'admingroup')

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('url', 'name')
    search_fields = ('url', 'name')

admin.site.register(Page, PageAdmin)
