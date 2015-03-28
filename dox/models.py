import datetime
import mimetypes
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dox import managers

# http://docs.djangoproject.com/en/dev/internals/contributing/#model-style
# https://code.djangoproject.com/browser/django/trunk/django/contrib/flatpages/models.py
# https://bitbucket.org/codekoala/django-articles/src/fc6a1ae96dc8/articles/models.py

class Page(models.Model):
    
    #----------------------------------
    # Hidden:
    #----------------------------------
    
    created  = models.DateTimeField(auto_now_add=True, editable=False,)
    modified = models.DateTimeField(auto_now=True, editable=False,)
    
    #----------------------------------
    # Base:
    #----------------------------------
    
    name          = models.CharField(_(u'name'), max_length=255, help_text=_(u'Page identifier, not published.'),)
    url           = models.CharField(_(u'URL'), max_length=255, unique=True, db_index=True, help_text=_(u'Example: /templates/ap/hosted2/ (leading/trailing slashes required)'),)
    template_name = models.CharField(_(u'template name'), max_length=70, blank=True, help_text=_(u"Example: 'contact_page.html'. If this isn't provided, the system will use 'default.html'."),)
    status        = models.ForeignKey('PageStatus', default='PageStatus.objects.default', help_text=_(u'Pages with non-"live" statuses will still be visible to super admins.'),)
    
    #----------------------------------
    # Scheduling:
    #----------------------------------
    
    is_active = models.BooleanField(_(u'active?'), default=True, blank=True, help_text=_(u'Disables/enables page for everyone (including super admins).'),)
    publish_date    = models.DateTimeField(_(u'publish date'), default=datetime.datetime.now, help_text=_(u'The date and time this page shall appear online.'),)
    expiration_date = models.DateTimeField(_(u'expiration date'), blank=True, null=True, help_text=_(u'Leave blank if the page does not expire.'),)
    
    #----------------------------------
    # Advanced:
    #----------------------------------
    
    login_required = models.BooleanField(_(u'login required'), blank=True, help_text=_(u'Enable this if users must login before they can read this article.'),)
    author         = models.ForeignKey(User, blank=True, null=True, help_text=_(u'For non-superusers to see their apps, this must be set to the desired non-superuser.'),)
    notes          = models.TextField(_(u'notes'), blank=True, help_text=_(u'Not published.'),)
    
    #----------------------------------
    # Head:
    #----------------------------------
    
    head_title        = models.CharField(_(u'title'), max_length=255, blank=True,)
    head_title_extra  = models.CharField(_(u'title extra'), max_length=255, blank=True, help_text=_(u'Example: " | The Register-Guard | Eugene, Oregon"'),)
    head_description  = models.CharField(_(u'description'), max_length=255, blank=True,)
    head_keywords     = models.CharField(_(u'keywords'), max_length=255, blank=True,)
    head_extra        = models.TextField(_(u'extra'), blank=True,)
    
    #----------------------------------
    # Body:
    #----------------------------------
    
    title             = models.CharField(_(u'title'), max_length=255, blank=True,)
    content           = models.TextField(_(u'content'), blank=True,)
    description_short = models.CharField(_(u'short description'), max_length=255, blank=True,)
    description_long  = models.TextField(_(u'long description'), blank=True,)
    extra             = models.TextField(_(u'extra'), blank=True,)
    
    objects = managers.PageManager()
    
    def __init__(self, *args, **kwargs):
        
        """Makes sure that we have some rendered content to use"""
        
        super(Page, self).__init__(*args, **kwargs)
        
        if self.pk:
            # mark the page as inactive if it's expired and still active
            if self.expiration_date and self.expiration_date <= datetime.datetime.now() and self.is_active:
                self.is_active = False
                self.save()
    
    class Meta:
        verbose_name = _(u'page')
        verbose_name_plural = _(u'pages')
        ordering = ('url',)
    
    @property
    def is_modified(self):
        return self.modified > self.created
    
    def __unicode__(self):
        return _(u'%s -- %s') % (self.name, self.url)
    
    def get_absolute_url(self):
        return ('/%s%s') % ('pages', self.url) # <-- This line, kinda funky...

class PageStatus(models.Model):
    
    name     = models.CharField(max_length=50,)
    ordering = models.IntegerField(default=0,)
    is_live  = models.BooleanField(default=False, blank=True,)
    
    objects = managers.PageStatusManager()
    
    class Meta:
        ordering = ('ordering', 'name',)
        verbose_name_plural = _(u'Page statuses')
    
    def __unicode__(self):
        if self.is_live:
            return u'%s (live)' % self.name
        else:
            return self.name

class File(models.Model):
    
    def upload_to(instance, filename):
        return 'dox/%s/%s' % (instance.page.pk, filename)
    
    uploaded = models.DateTimeField(auto_now_add=True,)
    modified = models.DateTimeField(auto_now=True,)
    file     = models.FileField(_(u'file'), upload_to=upload_to,)
    caption  = models.CharField(_(u'caption'), max_length=255, blank=True,)
    page     = models.ForeignKey('Page', related_name='files',)
    
    class Meta:
        ordering = ('-page', 'id',)
    
    def __unicode__(self):
        # return u'%s: %s, %s' % (self.title, os.path.basename(self.file.name), self.created.strftime('%Y-%m-%d %I:%M:%S'))
        return u'%s: %s' % (self.page.name, self.filename)
    
    @property
    def filename(self):
        return self.file.name.split('/')[-1]
    
    @property
    def content_type_class(self):
        mt = mimetypes.guess_type(self.file.path)[0]
        if mt:
            content_type = mt.replace('/', '_')
        else:
            # assume everything else is text/plain
            content_type = 'text_plain'
        
        return content_type
    
    @property
    def is_modified(self):
        return self.modified > self.uploaded