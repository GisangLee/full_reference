from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from utils.jwt import CustomJwtTokenAuthentication


class UserBaseViewSet(ModelViewSet):

    serializer_class = None
    read_serializer_class = None

    def get_serializer_class(self):
        """시리얼라이저 초기화

        Args:
            self

        요청 메서드 별로 각기 다른 시리얼라이저 부여

        """

        if self.request.method.lower() == "get":
            return self.read_serializer_class

        return self.serializer_class

    def get_authenticators(self):
        """authentication_classes 초기화

        Args:
            self

        요청 메서드 별로 각기 다른 인증 모듈 부여

        """

        print(f"요청 메서드 : {self.request.method}")

        if (
            self.request.method.lower() == "get"
            or self.request.method.lower() == "post"
        ):
            return []

        return [CustomJwtTokenAuthentication()]
