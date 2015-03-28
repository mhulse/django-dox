from django import shortcuts, template
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from dox.models import Page

# Copied from:
# https://code.djangoproject.com/browser/django/trunk/django/contrib/flatpages/views.py

DEFAULT_TEMPLATE = 'dox/default.html'

def page(request, url):
    
    # Add a beginning and (optional) ending slash:
    if not url.startswith('/'):
        url = '/' + url
    if not url.endswith('/') and settings.APPEND_SLASH:
        url += '/'
    
    # Get the page:
    try:
        f = Page.objects.live(user=request.user).get(url__exact=url)
    except Page.DoesNotExist:
        raise Http404
    
    """
    if not url.startswith('/'):
        url = '/' + url
    
    try:
        f = get_object_or_404(Page, url__exact=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(Page, url__exact=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    """
    
    return render_page(request, f)

@csrf_protect
def render_page(request, f):
    
    if f.login_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    
    if f.template_name:
        template = DEFAULT_TEMPLATE.replace('default.html', f.template_name) # Saves user from having to type "dox/" path.
        t = loader.select_template((template, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)
    
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)
    
    c = RequestContext(request, {
        'page': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)
    return response