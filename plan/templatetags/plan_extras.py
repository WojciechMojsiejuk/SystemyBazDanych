from django import template

register = template.Library()


@register.filter(name='space_to_new_line')
def replace_space(value):
    """Replaces all values of space from the given string with a line break."""
    return value.replace(' ', "\n")