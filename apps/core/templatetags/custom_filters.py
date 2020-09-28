from django import template
from django.conf import settings
import json

register = template.Library()


@register.filter(name="type")
def get_type(value):
    try:
        _message = json.loads(value.message)
        message = []
        for k, v in _message.items():
            message.append("{}: {}".format(k, v[0]['message']))

    except (json.decoder.JSONDecodeError, Exception):
        message = value.message

    return message


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
