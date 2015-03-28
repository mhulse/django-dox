# http://carsongee.com/blog/2010-06-30/64

from urllib2 import urlopen
from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.cache import cache

register = template.Library()

class RemoteInclude(template.Node):
    
    STALE_REFRESH = 1
    STALE_CREATED = 2
    ERROR_LOADING = _(u'Unable to retrieve remote file')
    
    def __init__(self, url, timeout=3600, should_cache=False):
        
        self.url = url
        self.should_cache = should_cache
        self.timeout = timeout
    
    def get_url(self):
        output = ''
        try:
            rf = urlopen(self.url, timeout=10)
            output = rf.read()
            rf.close()
        except IOError:
            output = self.ERROR_LOADING
        return output
    
    def render(self, context):
        output = ''
        if self.should_cache:
            cache_key = self.url + 'cg_ri'
            output = cache.get(cache_key)
            if output == None or output.decode('utf-8') == self.ERROR_LOADING:
                #print('retrieving from url')
                output = self.get_url()
                cache.set(cache_key, output, self.timeout)
            else:
                #print('retrieving from cache')
                output = cache.get(cache_key)
        else:
            output = self.get_url()
        return output

@register.tag
def sri(parser, token):
    
    '''
    Simple Remote Include, doesn't do any caching.
    Form: {% sri url %}
    '''
    
    bits = list(token.split_contents())
    
    if len(bits) != 2:
        raise template.TemplateSyntaxError, _(u'The %r tag takes one argument' % bits[0])
    
    if not (bits[1][0] == bits[1][-1] and bits[1][0] in ('"', "'")):
        raise template.TemplateSyntaxError, _(u'The %r tag\'s url should be in quotes' % bits[0])
    
    return RemoteInclude(bits[1][1:-1])

@register.tag
def cri(parser, token):
    
    '''
    Caching remote include - puts remote URL into a cache that expires in the 
    specified amount of time.
    Form: {% cri url timeout_in_seconds %}
    '''
    
    bits = list(token.split_contents())
    
    if len(bits) != 3:
        raise template.TemplateSyntaxError, _(u'The %r tag takes two arguments. The URL and the amount of time to cache the contents of the URL' % bits[0])
    
    try:
        timeout = int(bits[2])
    except ValueError:
        raise template.TemplateSyntaxError, _(u'The %r tag requires a valid integer in seconds for the cache timeout value: \'%s\' given' % (bits[0], bits[2]))
    
    if not (bits[1][0] == bits[1][-1] and bits[1][0] in ('"', "'")):
        raise template.TemplateSyntaxError, _(u'The %r tag\'s url should be in quotes' % bits[0])
    
    return RemoteInclude(url=bits[1][1:-1], timeout=int(bits[2]), should_cache=True)
