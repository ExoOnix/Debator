from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])


@register.filter(name="dict_value_or_null")
def dict_value_or_null(dict, key):
    if key in dict:
        return dict[key]
    else:
        return "null"
