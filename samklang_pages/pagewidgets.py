from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from samklang_pages.models import Page

class Widget(object):

    def __init__(self, options, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.options = options

    def get_display_name(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def render_option_form(self):
        raise NotImplementedError

    def get_option_dict(self):
        return self.options

class Image(Widget):
    """Image widget for adding an image"""

    def render(self):
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

    def render(self):
        url = self.options.get('url')
        try:
            page = Page.objects.get(url=url)
            return page.content_html
        except ObjectDoesNotExist:
            return u""


class Slider(Widget):
    def render(self):
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
