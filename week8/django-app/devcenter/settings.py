import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key-change-in-production")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() not in ("false", "0", "no")

_allowed_hosts_env = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_env.split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "corsheaders",
    "notes",
    "actionitems",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "devcenter.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

_cors_origins_env = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if _cors_origins_env:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
else:
    CORS_ALLOW_ALL_ORIGINS = True
