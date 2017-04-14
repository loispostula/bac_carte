from django import template
from django.template.defaultfilters import stringfilter

escape_chars = ["_"]

register = template.Library()
@register.simple_tag
def latex_escape(value):
    value = str(value)
    for c in escape_chars:
        value = value.replace(c, "\{}".format(c))
    return value

