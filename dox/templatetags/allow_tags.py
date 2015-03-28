from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# http://www.soyoucode.com/2011/set-variable-django-template
# http://djangosnippets.org/snippets/861/
# http://stackoverflow.com/questions/4183252/what-django-resolve-variable-do-template-variable
# https://docs.djangoproject.com/en/dev/ref/templates/api/

@register.tag
def allow_tags(parser, token):
    
    """
    Example: {% allow_tags page.content %}
    """
    
    try:
        # Splitting by None == splitting by spaces:
        tag_name, var_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires arguments' % token.contents.split()[0]
    
    return RenderNode(var_name)
allow_tags.is_safe = True

class RenderNode(template.Node):
    
    def __init__(self, content):
        self.content = content
    
    def render(self, context):
        try:
            content = template.Variable(self.content).resolve(context)
            return template.Template(content).render(template.Context(context, autoescape=False))
        except template.TemplateSyntaxError, e:
            return mark_safe('Template error: There is an error one of this page\'s template tags: <code>%s</code>' % e.message)