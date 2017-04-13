from django import template
from django.template.defaultfilters import stringfilter

escape_chars = ["_"]

register = template.Library()
@register.filter
def latex_escape(value):
    for c in escape_chars:
        value = value.replace(c, "\{}".format(c))
    return value

