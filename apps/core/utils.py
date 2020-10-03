from django.conf import settings
import pytz
import datetime

timezone = pytz.timezone(settings.TIME_ZONE)


def today():
    return datetime.datetime.now().astimezone(timezone)
