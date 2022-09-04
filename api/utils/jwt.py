import os, jwt, datetime, time
from django.contrib.auth import get_user_model
from rest_framework import exceptions
import logging as log

logger = log.getLogger("django.request")

# JWT 발급 시스템
def generate_jwt_token(payload, type):
    SECONDS = 1
    MINUTE = SECONDS * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    MONTH = DAY * 30
    YEAR = DAY * 365

    JWT_SECRET = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("JWT_ALGORITHM")

    if type == "access":
        # exp = datetime.datetime.now() + datetime.timedelta(seconds=3)
        # 만료 토큰 생명 주기 한 달
        exp = int(time.time()) + (MONTH)

    elif type == "refresh":
        # 갱신 토큰 생명 주기 한 달 + 1주
        exp = int(time.time()) + (MONTH + (DAY * 7))

    else:
        raise Exception("토큰 타입을 정확하게 명시해 주세요.")

    payload["exp"] = exp
    payload["iat"] = datetime.datetime.now()
    jwt_encoded = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    return jwt_encoded


class CustomJwtTokenAuthentication(object):

    keyword = "jwt"

    user_model = get_user_model()

    def __init__(self):
        self.__JWT_SECRET = os.environ.get("SECRET_KEY")
        self.__ALGORITHM = os.environ.get("JWT_ALGORITHM")

    JWT_SECRET = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("JWT_ALGORITHM")

    def __get_authorization_header(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION")
        return auth

    def authenticate(self, request):
        token = self.__get_authorization_header(request)

        if not token:
            raise exceptions.AuthenticationFailed("사용자를 인증할 수 없습니다.")

        token = token.replace("jwt ", "")
        logger.debug(
            {
                "JWT": token,
            }
        )
        # 토큰 디코딩
        payload = jwt.decode(token, self.__JWT_SECRET, algorithms=self.__ALGORITHM)

        # 토큰 만료 데이터 파싱
        expire = payload.get("exp")

        # 현재 시간
        cur_date = int(time.time())

        # 토큰 만료 처리
        if cur_date > expire:
            return None

        # 유저 객체
        user_id = payload.get("user_id")

        if not user_id:
            return None

        try:
            user = self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed("사용자가 존재하지 않습니다.")

        return (user, token)

    def authenticate_header(self, request):
        return self.keyword
