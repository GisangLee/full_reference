# Python Built-in Packages


# Django Packages
import logging as log
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Custom Packages
from accounts import models as account_models
from accounts.serializers import serializer as account_ser
from utils import mixins as util_mixins
from utils.errors import Error
from utils.success import Success
from utils.swaggers.accounts import doc as swag_account_doc
from utils.perms import owner_only


logger = log.getLogger("django.request")


class UserViewSet(util_mixins.BaseViewSet):

    queryset = account_models.User.objects.prefetch_related("profile_images").filter(
        is_deleted=False
    )
    read_serializer_class = account_ser.ReadUserSerializer
    serializer_class = account_ser.UserSerializer

    def get_queryset(self):
        return super().get_queryset()

    def __detail_queryset(self, pk):
        try:

            user = account_models.User.objects.prefetch_related("profile_images").get(
                pk=pk
            )

            if user:
                return user

        except account_models.User.DoesNotExist:
            return None

    @swagger_auto_schema(
        manual_parameters=swag_account_doc.list_users,
        tags=["사용자 리스트업"],
        operation_description="사용자 정보 불러오기 ",
    )
    def list(self, request):

        users = self.get_queryset()
        users = list(users)

        user_json = self.read_serializer_class(users, many=True)

        return Response(
            Success.response(
                self.__class__.__name__, request.method, user_json.data, "200"
            ),
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        manual_parameters=swag_account_doc.signup,
        tags=["회원가입"],
        operation_description="회원가입",
    )
    def create(self, request, *args, **kwargs):

        new_user = self.serializer_class(data=request.data)

        if new_user.is_valid():
            new_user.save()
            return Response(
                Success.response(
                    self.__class__.__name__, request.method, new_user.data, "200"
                ),
                status=status.HTTP_201_CREATED,
            )

        return Response(
            Error.error(new_user.errors), status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, pk):

        query = self.__detail_queryset(pk)

        if query is None:

            return Response(
                Error.error("사용자가 존재하지 않습니다."), status=status.HTTP_400_BAD_REQUEST
            )

        user_json = self.read_serializer_class(query)

        return Response(
            Success.response(
                self.__class__.__name__, request.method, user_json.data, "200"
            )
        )

    @method_decorator(owner_only, name="dispatch")
    def partial_update(self, request, *args, **kwargs):

        return super().partial_update(request, *args, **kwargs)

    @method_decorator(owner_only, name="dispatch")
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

    @method_decorator(owner_only, name="dispatch")
    def delete(self, request, *args, **kwargs):

        logged_in_user = request.user

        logged_in_user.is_deleted = True

        logged_in_user.save()

        return Response(
            Success.response(
                self.__class__.__name__, request.method, "계정이 탈퇴되었습니다.", "200"
            ),
            status=status.HTTP_200_OK,
        )
