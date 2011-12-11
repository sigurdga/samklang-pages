from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from samklang_menu.widgets import Widget
from samklang_pages.models import Page


class Image(Widget):
    """Image widget for adding an image"""

    def render(self, request):
        #print self.options
        retval = u"""
<img class="%(class)s" src="%(src)s" alt="%(alt)s" />
        """ % {
            'class': self.options.get('class', ''),
            'src': self.options.get('src', ''),
            'alt': self.options.get('alt', ''),
        }
        return retval

class StaticPage(Widget):
    """Fill in the contents of another static page into a widget"""

    def render(self, request):
        url = self.options.get('url')
        try:
            page = Page.objects.get(site=request.site, url=url)
            if not page.group or page.group in request.user.groups.all():
                ret = '<div class="widget">'
                if request.user.is_superuser:
                    ret += '<div class="widget-context-menu"><a href="%(edit-url)s" title="%(edit-help-text)s">%(edit-link-text)s</a></div>' % {
                        'edit-url': reverse('pages-page-edit', args=(page.id,)),
                        'edit-help-text': _('Edit'),
                        'edit-link-text': "&#9998;",
                        }
                ret += '%(content)s</div>' % {
                        'content': page.content_html,
                        }
                return ret
            else:
                return ""
        except ObjectDoesNotExist:
            return u""


class Slider(Widget):
    def render(self, request):
        """Render slider widget using options from json field"""

        javascript = u"""
        <script src="%(STATIC_URL)sjs/slides.min.jquery.js"></script>
		<script>
    		$(function(){
    			$('#slides').slides({
    				preload: true,
                    preloadImage: '%(STATIC_URL)simg/loading.gif',
    				play: 8000,
    				pause: 2000,
    				hoverPause: true,
    				animationStart: function(current){
    					$('.caption').animate({
    						bottom:-35
    					},100);
    				},
    				animationComplete: function(current){
    					$('.caption').animate({
    						bottom:0
    					},200);
    				},
    				slidesLoaded: function() {
    					$('.caption').animate({
    						bottom:0
    					},200);
    				}
    			});
    		});
    	</script>
        """ % {"STATIC_URL": settings.STATIC_URL}

        slides = [ u"""<div class="slide"><a href="%(url)s" title="%(title)s"><img src="%(src)s" width="386" height="283" alt="%(alt)s"></a><div class="caption" style="bottom:0"><p>%(title)s</p></div></div>""" % {'url': slide.get('url', slide.get('src')), 'title': slide.get('title', ''), 'alt': slide.get('alt', slide.get('title', '')), 'src': slide.get('src', '') } for slide in self.options.get("slides") ]

        html = u"""<div id="slides"><div class="slides_container">""" + "".join(slides) + u"""</div></div><img src="/static/img/frame.png" width="452" height="338" alt="Frame" id="frame">"""

        return javascript + html
