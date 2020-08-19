# from .apps.core.helper import get_subdomain
# from .threadlocal import thread_local
# """
# Swtich the middleware to change from
# 'Single Schema' to 'Multi Db' multitenancy
# """
#
#
# def multidb_middleware(get_response):
#     def middleware(request):
#         subdomain = get_subdomain(request)
#         request.customer = subdomain
#
#         @thread_local(using_db=subdomain)
#         def execute_request(request):
#             return get_response(request)
#
#         response = execute_request(request)
#         return response
#
#     return middleware

from django.utils import translation
from django.conf import settings


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
