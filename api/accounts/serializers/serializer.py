import logging as log
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from accounts import models as account_models
from utils.jwt import generate_jwt_token

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
    profile = serializers.CharField(write_only=True, max_length=255)

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

        new_user.gender = validate_data["gender"]
        new_user.age = validate_data["age"]

        if validate_data["profile"] is not None or validate_data["profile"] != "":

            account_models.UserProfile.objects.create(
                user=new_user, avatar=validate_data["profile"]
            )

        new_user.set_password(validate_data["password"])
        new_user.save()

        return new_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            response = {
                "message": "등록된 사용자가 아닙니다. 회원가입을 진행해 주세요.",
                "token": "",
                "status": 400,
                "user_id": "",
            }
            return response

        payload = {"user_id": user.id}
        access_jwt_token = generate_jwt_token(payload, "access")

        update_last_login(None, user)

        response = {
            "message": "OK",
            "token": access_jwt_token,
            "status": 200,
            "user_id": user.id,
        }
        return response
