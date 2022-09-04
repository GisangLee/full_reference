import time
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from accounts import models as account_models
from accounts.serializers import serializer as account_ser
from utils import mixins as util_mixins
from utils.errors import Error
from utils.success import Success


class UserViewSet(util_mixins.BaseViewSet):

    queryset = account_models.User.objects.prefetch_related("profiles").all()
    read_serializer_class = account_ser.ReadUserSerializer
    serializer_class = account_ser.UserSerializer

    def get_queryset(self):
        return super().get_queryset()

    def __detail_queryset(self, pk):
        try:

            user = account_models.User.objects.prefetch_related("profiles").get(pk=pk)

            if user:
                return user

        except account_models.User.DoesNotExist:
            return None

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
