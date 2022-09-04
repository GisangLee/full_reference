from rest_framework import serializers
from accounts import models as account_models


class ReadUserPorifleSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.UserProfile
        fileds = (
            "pk",
            "avatar",
            "created_at",
            "updated_at",
        )


class ReadUserSerializer(serializers.ModelSerializer):

    profile = ReadUserPorifleSerializer(read_only=True)

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
    profile = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = account_models.User
        fields = (
            "username",
            "email",
            "gender",
            "age",
            "profile",
        )
