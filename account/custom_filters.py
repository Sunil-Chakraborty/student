from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def striptags_with_nbsp(value):
    stripped_content = strip_tags(value)
    return mark_safe(stripped_content.replace('&nbsp;', ' '))
