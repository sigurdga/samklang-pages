from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from samklang_pages.models import Page

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
