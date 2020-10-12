from apps.core.utils import get_subdomain
from .threadlocal import thread_local
from django.utils import timezone
from django.utils import translation
from django.conf import settings
import pytz


class LocaleMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        # language = translation.get_language_from_request(request)
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG

    def process_response(self, request, response):
        translation.deactivate()
        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


def multidb_middleware(get_response):
    def middleware(request):
        subdomain = get_subdomain(request)
        # customer = get_customer(subdomain)
        # request.customer = customer
        request.customer = subdomain

        # @thread_local(using_db=customer.name)
        @thread_local(using_db=subdomain)
        def execute_request(request):
            return get_response(request)

        response = execute_request(request)
        return response
    return middleware


def tenant_middleware(get_response):
    def middleware(request):
        # we are going to use subdomains to identify customers.

        # the first step is to extract the identifier from the url
        host = request.get_host()  # here is the full url, something like this: 'https://ibm.spinnertracking.com'
        host = host.split(':')[1]  # we remove the protocol part: 'ibm.spinnertracking.com'
        subdomain = host.split('.')[0]  # and now we get the subdomain:'ibm'

        # now is just a matter of using the subdomain to find the
        # corresponding Customer in our database
        # try:
        #     customer = Customer.objects.get(name=subdomain)
        # except Customer.DoesNotExist:
        #     customer = None
        # and it to the request
        # request.tenant = customer
        request.tenant = subdomain

        # all done, the view will receive a request with a tenant attribute
        return get_response(request)
    return middleware
