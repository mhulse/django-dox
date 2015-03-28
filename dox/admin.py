import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from dox.models import Page, PageStatus, File
from dox.forms import PageForm

# https://bitbucket.org/codekoala/django-articles/src/fc6a1ae96dc8/articles/admin.py

#--------------------------------------------------------------------------
#
# Model inlines:
#
#--------------------------------------------------------------------------

class FileInline(admin.TabularInline):
    
    fields = ('file', 'caption',)
    
    model = File
    extra = 1

#--------------------------------------------------------------------------
#
# Admin models:
#
#--------------------------------------------------------------------------

class PageAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    fieldsets = [
        
        (None, {
            'fields': [
                'name',
                'url',
                'template_name',
                'status',
            ],
        }),
        
        ('Scheduling', {
            'fields': [
                'is_active',
                'publish_date',
                'expiration_date',
            ],
        }),
        
        ('Head', {
            'fields': [
                'head_title',
                'head_title_extra',
                'head_description',
                'head_keywords',
                'head_extra',
            ],
        }),
        
        ('Body', {
            'fields': [
                'title',
                'description_short',
                'description_long',
                'content',
                'extra',
            ],
        }),
        
        ('Advanced', {
            'fields': [
                'login_required',
                'author',
                'notes',
            ], 'classes': ['collapse'],
        }),
        
    ]
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = PageForm
    
    #----------------------------------
    # Inlines:
    #----------------------------------
    
    inlines = [
        FileInline,
    ]
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display       = ('name', 'url', 'template_name', 'status', 'author', 'publish_date', 'expiration_date', 'is_active',)
    list_display_links = ('name', 'status', 'is_active', 'publish_date', 'expiration_date',)
    list_editable      = ('url', 'template_name', 'author',)
    list_filter        = ('author', 'status', 'is_active', 'publish_date', 'expiration_date',)
    
    date_hierarchy = 'publish_date'
    
    search_fields = (
        'notes',
        'name',
        'url',
        'title',
        'content',
        'template_name',
        'head_title',
        'head_title_extra',
        'head_description',
        'head_keywords',
        'head_extra',
        'description_short',
        'description_long',
        'extra',
    )
    
    actions = ['mark_active', 'mark_inactive',]
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    
    #----------------------------------
    # Change list actions:
    #----------------------------------
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = _(u'Mark select articles as active')
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = _(u'Mark select articles as inactive')
    
    def get_actions(self, request):
        actions = super(PageAdmin, self).get_actions(request)
        def dynamic_status(name, status):
            def status_func(self, request, queryset):
                queryset.update(status=status)
            status_func.__name__ = name
            status_func.short_description = _(u'Set status of selected to "%s"' % status)
            return status_func
        for status in PageStatus.objects.all():
            name = 'mark_status_%i' % status.id
            actions[name] = (dynamic_status(name, status), name, _(u'Set status of selected to "%s"' % status))
        return actions
    
    #----------------------------------
    # Change forms:
    #----------------------------------
    
    save_on_top = True
    save_as     = True
    
    #----------------------------------
    # Methods:
    #----------------------------------
    
    def queryset(self, request):
        """
        Limit the list of articles to article posted by this user unless they're a superuser.
        """
        if request.user.is_superuser:
            return self.model._default_manager.all()
        else:
            return self.model._default_manager.filter(author=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Restrict the list of authors to Super Users and Staff only.
        """
        if db_field.name == 'author':
            '''
            Query filters out DTI Django Users and alphabetizes result.
            '''
            kwargs['queryset'] = User.objects.filter(is_staff=True, email__contains='registerguard.com').order_by('username')
        
        return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class PageStatusAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = ('name', 'is_live')
    list_filter  = ('is_live',)
    
    search_fields = (
        'name',
    )

class FileAdmin(admin.ModelAdmin):
    
    pass

#--------------------------------------------------------------------------
#
# Registrations:
#
#--------------------------------------------------------------------------

admin.site.register(Page, PageAdmin)
admin.site.register(PageStatus, PageStatusAdmin)
admin.site.register(File, FileAdmin)