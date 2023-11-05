"""
Django settings for feleexpress project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import datetime
import os
from pathlib import Path

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS_STRING = config("ALLOWED_HOSTS_STRING", default="")
if not ALLOWED_HOSTS_STRING:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(",")

# Base User
AUTH_USER_MODEL = "authentication.User"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework",
    "drf_yasg",
    "authentication.apps.AuthenticationConfig",
    "customer.apps.CustomerConfig",
    "rider.apps.RiderConfig",
    "wallet.apps.WalletConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "feleexpress.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "feleexpress.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_URL = config("DATABASE_URL", default="")

# set db connection requests to 600 seconds to enable persistent connections
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=0)}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ENVIRONMENT = config("ENVIRONMENT", default="dev")  # dev or production or staging

REDIS_CONNECTION_URL = config("REDIS_URL", default="redis://127.0.0.1:6379")
REDIS_INSTANCE_ONE = f"{REDIS_CONNECTION_URL}/0"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_INSTANCE_ONE,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "helpers.utils.CustomPagination",
    "PAGE_SIZE": 8,
    "EXCEPTION_HANDLER": "helpers.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": f"{config('THROTTLE_RATE', default='1000')}/{config('THROTTLE_PERIOD', default='day')}",
        "user": f"{config('THROTTLE_RATE', default='1000')}/{config('THROTTLE_PERIOD', default='day')}",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME", default=60, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(
        minutes=config("REFRESH_TOKEN_LIFETIME", default=360, cast=int)
    ),
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_TOKEN_CLASSES": ("helpers.token_manager.CustomAccessToken",),
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")

ACCOUNT_SID = config("ACCOUNT_SID", "")
AUTH_TOKEN = config("AUTH_TOKEN", "")
VERIFY_SID = config("VERIFY_SID", "")
SMS_FROM = config("SMS_FROM", "")

SENDGRID_API_KEY = config("SENDGRID_API_KEY", "")
SENDER_EMAIL = config("SENDER_EMAIL", "")
SENDER_NAME = config("SENDER_NAME", "")

AWS_DEFAULT_REGION = config("AWS_DEFAULT_REGION", "")
AWS_S3_BUCKET = config("AWS_S3_BUCKET", "")
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "")

EMAIL_VERIFICATION_TTL = config("EMAIL_VERIFICATION_TTL", 21600, cast=int)
EMAIL_VERIFICATION_MAX_TRIALS = config("EMAIL_VERIFICATION_MAX_TRIALS", 5, cast=int)

PHONE_VERIFICATION_TTL = config("PHONE_VERIFICATION_TTL", 21600, cast=int)
PHONE_VERIFICATION_MAX_TRIALS = config("PHONE_VERIFICATION_MAX_TRIALS", 3, cast=int)

TEST_OTP = config("TEST_OTP", "376213", cast=str)
PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY")
