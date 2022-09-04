from rest_framework import status
from rest_framework.response import Response
from utils.errors import Error
from accounts import models as account_models


def owner_only(func):
    def wrapper_func(*args, **kwargs):

        request = args[0]

        # logged_in_user = request.user
        logged_in_user = request.user
        target_id = kwargs.get("pk")

        if int(logged_in_user.id) != int(target_id):
            return Response(
                Error.errors("권한이 없습니다"), status=status.HTTP_401_UNAUTHORIZED
            )

        return func(*args, **kwargs)

    return wrapper_func
