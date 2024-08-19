"""
Django settings for vaso project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from envparse import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)qzq##2f48ch)2wm@b&1_44sxh5c_+#(bb2&@qm)x$&)=b6pan"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    "main.apps.MainConfig",
    "user.apps.UserConfig",
    "catalog.apps.CatalogConfig",
    'orders.apps.OrdersConfig'

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

ROOT_URLCONF = "vaso.urls"

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

WSGI_APPLICATION = "vaso.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join("static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join("media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field


HOST = env.str('HOST', default='https://localhost')

CSRF_TRUSTED_ORIGINS = [HOST]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AMOCRM_CLIENT_ID = 'b6932d47-1674-4eba-8199-0a8607b70693'
AMOCRM_CLIENT_SECRET = 'TlJDbpRBecC7XIDVv2VcovcCp1VIxaDWf3Fq6XMSq4PvcTggDccL70msq9TlXlWd'
AMOCRM_REDIRECT_URI = 'https://vaso.site/'
AMOCRM_SUBDOMAIN = 'vasoproject'
AMOCRM_TOKEN = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImM3YTFiOTg1ZTY0Zjk3MDRhYTdlMjQyZjAzZTRmYmQxNWJiMDFlNWY4N'
                '2M4MmM4ZjUwYTNmZWUzNzhmNmY3ZmQzMWQxOTJkNGMzZjczMDcyIn0.eyJhdWQiOiJiNjkzMmQ0Ny0xNjc0LTRlYmEtODE5OS0wYT'
                'g2MDdiNzA2OTMiLCJqdGkiOiJjN2ExYjk4NWU2NGY5NzA0YWE3ZTI0MmYwM2U0ZmJkMTViYjAxZTVmODdjODJjOGY1MGEzZmVlMzc'
                '4ZjZmN2ZkMzFkMTkyZDRjM2Y3MzA3MiIsImlhdCI6MTcyMzU0NDM5OCwibmJmIjoxNzIzNTQ0Mzk4LCJleHAiOjE4ODAyMzY4MDAs'
                'InN1YiI6IjExMjY5OTgyIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxODQ3MzAyLCJiYXNlX2RvbWFpbiI6ImFtb2Nyb'
                'S5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdX'
                'NoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiMTUwNmRhMzEtZDM0ZS00MjQwLTgzMTctNDdjNGRlYmVmZjEzIn0.gwtwLQf'
                'lcgpGL1H3B7BsAtIPG1KhqiqE8wcSeP0uETKD65s8Yl9iKkU32DSZy7UCPcl-5-cZt7NeQdbssR6tNVWaFLyJPt3X15o2GdECrT_b'
                'Tt2jkiT3jFWCDdSDgHCHivNNfzKbEPfPZ3yRgX2lN5Ye_RUeqgWGBv6GtBuOzofYiEQsE52uWt1SJfTw5_sq034P06qMUxRfxhRCy'
                'J2EZ9EWK1R0mo-brnG6vwGW_Rz8iFOx9ol7a2U6zMcchM3BRd9USP7O1GLzPQtiaC5n59IYbGuigui4cVKvalmYldd0wsATjpUhBF'
                '6K03DtTWFcyIsx8GbiqmHr7PfI7I_qEg')
