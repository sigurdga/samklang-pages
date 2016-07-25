from functools import partial
import re

from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db.models.query_utils import Q
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import simplejson

from samklang_pages.models import Page
from samklang_pages.forms import PageForm
from samklang_menu.models import Menu

WIDGET_REGEX = re.compile(r'!\{(\w+\.\w+)(?:\s+(.*?))?\}')
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

def widget_replace(request, matchobj):
    widget_name, widget_context = matchobj.group(1, 2)
    widget_context = "{" + widget_context + "}"
    app, widget_name = widget_name.rsplit(".", 1)
    imp = __import__(app + ".widgets", globals(), locals(), [widget_name])
    widget_class = getattr(imp, widget_name, None)
    if widget_class:
        try:
            options = simplejson.loads(widget_context)
        except:
            options = {}
        return widget_class(options).render(request)
    else:
        return ""

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
    rendered = t.render(c)
    rendered_replaced = WIDGET_REGEX.sub(partial(widget_replace, request), rendered)
    response = HttpResponse(rendered_replaced)
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
