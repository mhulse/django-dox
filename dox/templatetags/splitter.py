from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='splitter')
@stringfilter
def splitter(value, arg):
    return value.split(arg)
