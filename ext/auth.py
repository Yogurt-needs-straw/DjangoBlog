from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from api import models


class BlogAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """

        token = request.query_params.get("token")
        if not token:
            return

        instance = models.UserInfo.objects.filter(token=token).first()
        if not instance:
            return

        return instance,token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """

        return "API"

class NoAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """

        raise exceptions.AuthenticationFailed({"code": 2000, "error": "认证失败"})

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """

        return "API"


