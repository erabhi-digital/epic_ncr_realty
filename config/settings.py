"""
Django settings for config project.

Environment-aware settings for epic_ncr_realty.
Controlled via the ENVIRONMENT variable ("development" or "production"),
NOT tied directly to DEBUG anymore — this avoids the common mistake of
accidentally shipping DEBUG=True to production or vice versa.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================
# Loads variables from a .env file in the project root.
# On PythonAnywhere / production servers, real environment
# variables set on the server will always take priority
# over anything in the .env file.

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # "development" | "production"
IS_PRODUCTION = ENVIRONMENT == "production"


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-CHANGE-ME-this-is-a-dev-only-fallback",
)

# DEBUG is driven by env var, defaults safely to False.
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost",
).split(",")


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "model",
    "app",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI / ASGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# =========================================================
# DATABASE
# =========================================================
# Switched on ENVIRONMENT, not DEBUG — so you can run
# DEBUG=True against MySQL locally if needed, without it
# silently switching back to SQLite.

if not IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

# Source static directory (only used when it actually exists,
# avoids a warning on fresh checkouts before assets are added)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Production collected static files
STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# STATIC FILE STORAGE
# =========================================================
# Compressed + hashed filenames in production for cache-busting
# and smaller payloads. Plain storage in development so you don't
# need to run collectstatic on every change.

if IS_PRODUCTION:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": (
                "whitenoise.storage."
                "CompressedManifestStaticFilesStorage"
            ),
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage."
                "StaticFilesStorage"
            ),
        },
    }


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# CACHE
# =========================================================
# LocMemCache for development. Production uses the same
# backend by default but can be swapped for Redis/Memcached
# by setting CACHE_BACKEND / CACHE_LOCATION in .env.

CACHES = {
    "default": {
        "BACKEND": os.getenv(
            "CACHE_BACKEND",
            "django.core.cache.backends.locmem.LocMemCache",
        ),
        "LOCATION": os.getenv("CACHE_LOCATION", "app-local-cache"),
    },
}


# =========================================================
# EMAIL
# =========================================================

if not IS_PRODUCTION:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "noreply@modernestate.local"
    SERVER_EMAIL = "server@modernestate.local"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
    SERVER_EMAIL = os.getenv("SERVER_EMAIL", EMAIL_HOST_USER)


# =========================================================
# LOGGING
# =========================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "realestate": {
            "handlers": ["console"],
            "level": "DEBUG" if not IS_PRODUCTION else "INFO",
            "propagate": False,
        },
    },
}


# =========================================================
# CSRF / TRUSTED ORIGINS
# =========================================================

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://epicncrrealty.com,https://www.epicncrrealty.com",
).split(",")

if not IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS += [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]


# =========================================================
# HTTPS / SECURITY
# =========================================================

SECURE_SSL_REDIRECT = IS_PRODUCTION

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"


# =========================================================
# HSTS
# =========================================================

if IS_PRODUCTION:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False


# =========================================================
# SECURITY HEADERS
# =========================================================

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"