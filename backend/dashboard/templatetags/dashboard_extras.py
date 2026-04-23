"""
Template helpers used by the dashboard partials.
Currently provides:
  * `|index:i`        — list[i] lookup for templates (Django has none)
  * `|getitem:key`    — dict[key] lookup, same idea
"""
from django import template

register = template.Library()


@register.filter
def index(value, i):
    """Return value[i] or empty string on any error."""
    try:
        return value[int(i)]
    except (IndexError, KeyError, TypeError, ValueError):
        return ""


@register.filter
def getitem(value, key):
    """Return value[key] from a dict, or empty string."""
    try:
        return value[key]
    except (KeyError, TypeError):
        return ""
