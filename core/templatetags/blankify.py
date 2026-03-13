from django import template

register = template.Library()

@register.filter
def blankify(value):
    """
    Returns an empty string instead of None or the literal 'None'.
    """
    if value is None:
        return ""
    if isinstance(value, str) and value.strip().lower() == "none":
        return ""
    return value