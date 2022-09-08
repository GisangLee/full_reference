import copy
import os, jwt, datetime, time
from django.contrib.auth import get_user_model
from rest_framework import exceptions
import logging as log

logger = log.getLogger("django.request")

# JWT 발급 시스템
def generate_jwt_token(payload):
    # if type == "access":
    #     # exp = datetime.datetime.now() + datetime.timedelta(seconds=3)
    #     # 만료 토큰 생명 주기 일주일
    #     exp = int(time.time()) + (DAY * 7)

    # elif type == "refresh":
    #     # 갱신 토큰 생명 주기 일년
    #     exp = int(time.time()) + (YEAR)

    # if type is None or type == "":
    #     raise Exception("토큰 타입을 정확하게 명시해 주세요.")

    SECONDS = 1
    MINUTE = SECONDS * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    MONTH = DAY * 30
    YEAR = DAY * 365

    JWT_SECRET = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("JWT_ALGORITHM")

    access_token_expire_time = int(time.time()) + (DAY * 7)
    refresh_token_expire_time = exp = int(time.time()) + (YEAR)

    access_payload = copy.deepcopy(payload)
    refresh_payload = copy.deepcopy(payload)

    # access token 인코딩
    access_payload["exp"] = access_token_expire_time
    access_payload["iat"] = datetime.datetime.now()
    jwt_access_token_encoded = jwt.encode(
        access_payload, JWT_SECRET, algorithm=ALGORITHM
    )

    # refresh token 인코딩
    refresh_payload["exp"] = refresh_token_expire_time
    refresh_payload["iat"] = datetime.datetime.now()
    jwt_refresh_token_encoded = jwt.encode(
        refresh_payload, JWT_SECRET, algorithm=ALGORITHM
    )
    token = {
        "access_token": jwt_access_token_encoded,
        "refresh_token": jwt_refresh_token_encoded,
    }

    return token


def generate_access_token_by_refresh_token(payload: dict) -> dict:
    SECONDS = 1
    MINUTE = SECONDS * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    MONTH = DAY * 30
    YEAR = DAY * 365

    JWT_SECRET = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("JWT_ALGORITHM")

    access_token_expire_time = int(time.time()) + (DAY * 7)
    access_payload = copy.deepcopy(payload)

    access_payload["exp"] = access_token_expire_time
    access_payload["iat"] = datetime.datetime.now()
    jwt_access_token_encoded = jwt.encode(
        access_payload, JWT_SECRET, algorithm=ALGORITHM
    )

    token = {
        "access_token": jwt_access_token_encoded,
    }

    return token


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
