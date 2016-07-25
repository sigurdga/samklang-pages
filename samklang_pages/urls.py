from django.conf.urls import *
from samklang_pages.views import *

urlpatterns = patterns('samklang_pages.views',
    #(r'^(?P<url>.*)$', 'page'),
    url(r'new/$', PageCreateView.as_view(), name='pages-page-new'),
    url(r'edit/menu/(?P<page_id>\d+)/$', add_to_menu, name='pages-menu-add'),
    url(r'edit/(?P<pk>\d+)/$', PageUpdateView.as_view(), name='pages-page-edit'),
    url(r'$', PageListView.as_view(), name='pages-page-list'),
)
