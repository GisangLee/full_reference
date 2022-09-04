from rest_framework import serializers
from accounts import models as account_models
import logging as log

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
            "gender",
            "phone_number",
            "age",
            "is_deleted",
            "is_superuser",
            "created_at",
            "updated_at",
            "profile",
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
            "gender",
            "age",
            "profile",
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
