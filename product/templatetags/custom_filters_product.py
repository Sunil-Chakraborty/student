from django import template

register = template.Library()

@register.filter
def get_field_label(form, field_name):
    return form.fields[field_name].label
