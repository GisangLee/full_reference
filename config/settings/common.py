import os, dotenv, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJ_DIR = BASE_DIR.parent

sys.path.insert(0, os.path.join(PROJ_DIR, "api"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
    "rest_framework",
    "django_filters",
    "drf_yasg",
]

PROJ_APPS = [
    "accounts",
]

MIDDLEWARE = [
    "utils.middleware.ServiceHeaderMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(PROJ_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


"""
로거
"""

# Loggin 설정
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 형식정의
    "formatters": {
        "format1": {
            "format": "[%(asctime)s] %(levelname)s %(message)s\n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "format2": {
            "format": "-----" * 25 + "\n%(levelname)s %(message)s [%(name)s:%(lineno)s]"
        },
    },
    "handlers": {
        # 파일 저장
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(PROJ_DIR, "logs/full_ref.log"),
            "encoding": "UTF-8",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "format1",
        },
        # 콘솔(터미널)에 출력
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "format2",
        },
    },
    "loggers": {
        "django.server": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "": {  # root
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
    },
}


AUTH_USER_MODEL = "accounts.User"

# Authentication Customizing
AUTHENTICATION_BACKENDS = ("utils.login_auth.EmailUsernameLoginBackend",)
