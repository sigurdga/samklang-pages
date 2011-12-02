from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db.models.query_utils import Q
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from samklang_pages.models import Page
from samklang_pages.forms import PageForm
from samklang_menu.models import Menu

DEFAULT_TEMPLATE = 'samklang_pages/default.html'

def page(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    if hasattr(request, 'site'):
        f = get_object_or_404(Page, url__exact=url, site=request.site)
    else:
        f = get_object_or_404(Page, url__exact=url)
    if f.group and not f.group in request.user.groups.all():
        raise Http404
    return render_flatpage(request, f)

def render_flatpage(request, f):
    t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.name = mark_safe(f.name)
    f.content_html = mark_safe(f.content_html)

    c = RequestContext(request, {
        'page': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)
    return response

class PageCreateView(CreateView):
    model = Page
    form_class = PageForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.site = self.request.site
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.object.url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageCreateView, self).dispatch(*args, **kwargs)

class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm

    def get_success_url(self):
        return self.get_object().url

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageUpdateView, self).dispatch(*args, **kwargs)

class PageListView(ListView):
    model = Page

    def get_queryset(self):
        q = super(PageListView, self).get_queryset()
        return q.filter(Q(group=None) | Q(group__user=self.request.user))

def add_to_menu(request, page_id):
    if request.user.is_superuser:
        if request.method == 'GET' and 'parent_id' in request.GET:
            parent_id = request.GET['parent_id']
        else:
            parent_id = request.site.id
        parent = Menu.objects.get(pk=parent_id)
        page = Page.objects.get(pk=page_id)
        if not Menu.objects.filter(url=page.url):
            menuitem = Menu()
            menuitem.url = page.url
            menuitem.name = page.name
            menuitem.group = page.group
            menuitem.user = request.user
            menuitem.insert_at(parent, 'last-child', True)
        # TODO: make flash warning to show in redirect
    return HttpResponseRedirect(reverse("menu-list"))
