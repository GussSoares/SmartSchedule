from django.conf import settings
import pytz
import datetime

timezone = pytz.timezone(settings.TIME_ZONE)


def today():
    return datetime.datetime.now().astimezone(timezone)


def get_subdomain(request):
    if '192.168.' in request.get_host():
        return 'default'
    host = request.get_host().split(':')[0]
    subdomain = host.split('.')[0]
    if subdomain == 'localhost':
        return 'default'
    return subdomain
