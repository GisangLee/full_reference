from django.urls import is_valid_path
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import escape_leading_slashes
from django.core.exceptions import PermissionDenied
import logging as log

logger = log.getLogger("django.request")


class ServiceHeaderMiddleware(MiddlewareMixin):

    response_redirect_class = HttpResponsePermanentRedirect

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
        host = request.get_host()
        must_prepend = settings.PREPEND_WWW and host and not host.startswith("www.")
        redirect_url = ("%s://www.%s" % (request.scheme, host)) if must_prepend else ""

        # Check if a slash should be appended
        if self.should_redirect_with_slash(request):
            path = self.get_full_path_with_slash(request)
        else:
            path = request.get_full_path()

        # Return a redirect if necessary
        if redirect_url or path != request.get_full_path():
            redirect_url += path
            return self.response_redirect_class(redirect_url)

    def should_redirect_with_slash(self, request):
        """
        Return True if settings.APPEND_SLASH is True and appending a slash to
        the request path turns an invalid path into a valid one.
        """
        if settings.APPEND_SLASH and not request.path_info.endswith("/"):
            urlconf = getattr(request, "urlconf", None)
            if not is_valid_path(request.path_info, urlconf):
                match = is_valid_path("%s/" % request.path_info, urlconf)
                if match:
                    view = match.func
                    return getattr(view, "should_append_slash", True)
        return False

    def get_full_path_with_slash(self, request):
        """
        Return the full path of the request with a trailing slash appended.

        Raise a RuntimeError if settings.DEBUG is True and request.method is
        POST, PUT, or PATCH.
        """
        new_path = request.get_full_path(force_append_slash=True)
        # Prevent construction of scheme relative urls.
        new_path = escape_leading_slashes(new_path)
        if settings.DEBUG and request.method in ("POST", "PUT", "PATCH"):
            raise RuntimeError(
                "You called this URL via %(method)s, but the URL doesn't end "
                "in a slash and you have APPEND_SLASH set. Django can't "
                "redirect to the slash URL while maintaining %(method)s data. "
                "Change your form to point to %(url)s (note the trailing "
                "slash), or set APPEND_SLASH=False in your Django settings."
                % {
                    "method": request.method,
                    "url": request.get_host() + new_path,
                }
            )
        return new_path
