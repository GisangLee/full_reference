from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        try:
            user = self.model(
                email=self.normalize_email(email), username=username, **extra_fields
            )
            return user
        except Exception as e:
            print("CREATE USER ERROR : ", e)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            username=username, email=self.normalize_email(email)
        )

        superuser.is_superuser = True

        superuser.set_password(password)
        superuser.save(using=self.db)
        return superuser


class GenderChoices(models.TextChoices):

    MALE = "M", "남"
    FEMALE = "F", "여"


class User(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(max_length=20, unique=True, help_text="사용자 ID")
    email = models.EmailField(max_length=100, help_text="사용자 이메일")
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
        help_text="성별",
    )
    phone_number = models.CharField(
        max_length=255, blank=True, null=True, help_text="휴대폰 번호"
    )
    age = models.PositiveIntegerField(blank=True, null=True, help_text="나이")

    is_deleted = models.BooleanField(default=False, help_text="탈퇴 여부")
    is_superuser = models.BooleanField(default=False, help_text="시스템 관리자")
    is_admin = models.BooleanField(default=False, help_text="방 방장")
    is_manager = models.BooleanField(default=False, help_text="방 부방장")

    created_at = models.DateTimeField(auto_now_add=True, help_text="계정 생성 일자")
    updated_at = models.DateTimeField(auto_now=True, help_text="계정 수정 일자")

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        # return self.is_admin
        return True

    def has_perm(self, perm, obj=None):
        # return self.is_a
        return True


class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        related_name="profile_images",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="profile_images/%Y/%m/%d", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"


class JwtRefreshToken(models.Model):
    user = models.OneToOneField(
        User, related_name="refresh_token", on_delete=models.CASCADE
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = "jwt_refresh_token"
