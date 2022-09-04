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

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100)
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, blank=True, null=True
    )
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    avatar = models.ImageField(upload_to="profile_images/%Y/%m/%d")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"
