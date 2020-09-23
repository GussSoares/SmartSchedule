from django import template

register = template.Library()


@register.filter(name='get_all')
def get_all(value, arg):
    if arg == 'str':
        return ", ".join(value.values_list('first_name', flat=True))
    return ""
