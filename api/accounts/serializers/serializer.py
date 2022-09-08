import logging as log
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from accounts import models as account_models
from utils.jwt import generate_jwt_token, generate_access_token_by_refresh_token

logger = log.getLogger("django.request")


class ReadUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.UserProfile
        fields = (
            "pk",
            "avatar",
            "created_at",
            "updated_at",
        )


class ReadUserSerializer(serializers.ModelSerializer):

    # profile = ReadUserProfileSerializer(
    #     read_only=True, source="profile_images", many=True
    # )

    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        images = obj.profile_images.all()
        images = list(images)
        return ReadUserProfileSerializer(images[:10], many=True).data

    class Meta:
        model = account_models.User
        fields = (
            "pk",
            "username",
            "email",
            "profile",
            "gender",
            "age",
            "phone_number",
            "is_deleted",
            "is_admin",
            "is_manager",
            "is_superuser",
            "created_at",
            "updated_at",
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.CharField(
        write_only=True, max_length=255, help_text="프로필 이미지 주소"
    )

    class Meta:
        model = account_models.User
        fields = (
            "username",
            "email",
            "password",
            "profile",
            "gender",
            "age",
            "phone_number",
            "is_deleted",
            "is_admin",
            "is_manager",
            "is_superuser",
        )

    def __does_user_exists(self, username):

        try:
            user = account_models.User.objects.get(username=username)

            if user:
                return True

        except account_models.User.DoesNotExist:
            return False

    def create(self, validate_data):

        logger.debug({"validated_data": validate_data})

        user_exists = self.__does_user_exists(validate_data["username"])

        if user_exists:
            return False

        new_user = account_models.User.objects.create(
            username=validate_data["username"], email=validate_data["email"]
        )

        if validate_data["profile"] is not None or validate_data["profile"] != "":

            account_models.UserProfile.objects.create(
                user=new_user, avatar=validate_data["profile"]
            )

        new_user.set_password(validate_data["password"])
        new_user.gender = validate_data["gender"]
        new_user.age = validate_data["age"]
        new_user.phone_number = validate_data["phone_number"]
        new_user.is_deleted = validate_data["is_deleted"]
        new_user.is_admin = validate_data["is_admin"]
        new_user.is_manager = validate_data["is_manager"]
        new_user.is_superuser = validate_data["is_superuser"]

        new_user.save()

        return new_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def __save_refresh_to_db(self, user, refresh_token: str) -> int:

        try:

            exists_refresh_token = account_models.JwtRefreshToken.objects.get(
                token=refresh_token
            )

            print(f"exists_refresh_token : {exists_refresh_token}")

            if exists_refresh_token:

                return exists_refresh_token.pk

        except account_models.JwtRefreshToken.DoesNotExist:
            print(f"없다고?")
            refresh_token_instance = account_models.JwtRefreshToken.objects.create(
                user=user, token=refresh_token
            )

            return refresh_token_instance.pk

    def validate(self, data):

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            response = {
                "message": "등록된 사용자가 아닙니다. 회원가입을 진행해 주세요.",
                "access_token": None,
                "refresh_token": None,
                "status": 400,
                "user_id": None,
            }
            return response

        payload = {"user_id": user.id}
        # access_jwt_token = generate_jwt_token(payload, "access")

        jwt = generate_jwt_token(payload)

        access_token = jwt.get("access_token")
        refresh_token = jwt.get("refresh_token")

        refresh_token_idx = self.__save_refresh_to_db(user, refresh_token)
        update_last_login(None, user)

        response = {
            "message": "OK",
            "access_token": access_token,
            "refresh_token": refresh_token_idx,
            "status": 200,
            "user_id": user.id,
        }

        return response


class JwtSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(write_only=True)

    class Meta:
        model = account_models.JwtRefreshToken
        fields = ("pk",)


class ReadJwtSerializer(serializers.ModelSerializer):

    user = ReadUserSerializer()

    class Meta:
        model = account_models.JwtRefreshToken
        fields = (
            "pk",
            "user",
            "token",
            "created_at",
            "updated_at",
        )
