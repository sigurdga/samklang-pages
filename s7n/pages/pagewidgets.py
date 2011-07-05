from django.conf import settings

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
        print self.options
        retval = u"""
<img class="%(class)s" src="%(src)s" alt="%(alt)s" />
        """ % {
            'class': self.options.get('class', ''),
            'src': self.options.get('src', ''),
            'alt': self.options.get('alt', ''),
        }
        return retval


class Slider(Widget):

    def render(self):
        retval =  u"""
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

        <div id="slides">
<div class="slides_container">
<div class="slide">
<a href="http://nidarholm.no/" title="nidarholm.no" target="_blank"><img src="%(STATIC_URL)simg/nidarholm.no.png" width="386" height="283" alt="Skjermbilde nidarholm.no"></a>
<div class="caption" style="bottom:0">
<p>Nidarholm</p>
</div>
</div>
<div class="slide">
<a href="/static/img/moldejazzarkivet.png" title="Moldelazzarkivet" target="_blank"><img src="%(STATIC_URL)simg/moldejazzarkivet.png" width="386" height="283" alt="Skjermbilde Moldejazzarkivet"></a>
<div class="caption">
<p>Historisk arkiv for Moldejazz</p>
</div>
</div>
</div>
</div>
<img src="/static/img/frame.png" width="452" height="338" alt="Frame" id="frame">""" % {'STATIC_URL': settings.STATIC_URL}

        return retval
