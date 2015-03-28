from django.conf.urls.defaults import *

urlpatterns = patterns('dox.views',
    
    (r'^(?P<url>.*)$', 'page'),
    
)