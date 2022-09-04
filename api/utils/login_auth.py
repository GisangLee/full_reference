from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from accounts import models as accont_models

# 이메일 + 유저 ID 둘다 로그인 되도록 하는 커스텀 인증 시스템 구축
class EmailUsernameLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if "@" in username:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        try:
            user = get_user_model().objects.get(**kwargs)

            if user.check_password(password):
                return user

            else:
                # 비밀번호 오류 시 로그인 시도 횟수 증가
                return None

        except accont_models.User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
