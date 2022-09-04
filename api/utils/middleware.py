from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.conf import settings
import logging as log

logger = log.getLogger("django.request")


class ServiceHeaderMiddleware(MiddlewareMixin):

    response_redirect_class = HttpResponsePermanentRedirect

    def __init__(self, get_response):
        self.get_response = get_response
        # 최초 설정 및 초기화

    def __call__(self, request):
        # Exit out to async mode, if needed
        response = None

        if hasattr(self, "process_request"):

            response = self.process_request(request)

        response = response or self.get_response(request)

        print(f" res : {response}")

        return response

    def __get_http_header(self, request):
        system_key = request.META.get("HTTP_SYSTEM_KEY")
        return system_key

    def process_request(self, request):
        system_key = self.__get_http_header(request)

        if system_key is None:

            if not settings.DEBUG:
                raise PermissionDenied("secure key is needed")

        logger.debug(
            {
                "Middleware system key": system_key,
            }
        )
