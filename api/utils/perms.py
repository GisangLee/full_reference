from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from utils.errors import Error
from accounts import models as account_models


def owner_only(func):
    def wrapper_func(*args, **kwargs):
        """소유자 전용 퍼미션

        Args:
            args: 아규먼트
            kwargs: 키워드 아규먼트

        Returns:
            func : 소유자 전용 퍼미션 함수 이후에 실행할 내부 함수

        owner_only에 인자로 넘어온 함수를 실항하기 전,
        wrapper_func을 수행하여 소유자인지 체크 후,
        소유자 일 경우에만 인자로 받은 함수 실행

        """

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


def allow_any(func):
    def wrapper_func(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper_func


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_superuser == True


class ActiveUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_deleted == False


class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):

        return True
