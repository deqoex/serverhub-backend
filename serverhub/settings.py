"""
ServerHub — Django Settings
Production (Render) + Development (localhost) destekli
"""

import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Güvenlik ──────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-SADECE-GELISTIRME-ICIN')
DEBUG      = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1'
).split(',')

# ── Uygulamalar ───────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3. taraf
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # Kendi uygulamalarımız
    'apps.users',
    'apps.servers',
    'apps.ads',
    'apps.scraper',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # En üstte olmalı
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',     # Static dosyalar için
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'serverhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'serverhub.wsgi.application'

# ── Veritabanı ────────────────────────────────────────────────
# Render'da DATABASE_URL otomatik set edilir.
# Lokalde .env'deki DB_* değerlerini kullanır.

import dj_database_url

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Production (Render) — DATABASE_URL'den otomatik parse
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development (localhost)
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     config('DB_NAME',     default='serverhub'),
            'USER':     config('DB_USER',     default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='postgres'),
            'HOST':     config('DB_HOST',     default='localhost'),
            'PORT':     config('DB_PORT',     default='5432'),
        }
    }

# ── Auth ──────────────────────────────────────────────────────
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── DRF ──────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'vote': '1/day',
    },
}

# ── CORS ──────────────────────────────────────────────────────
# Render'da CORS_ORIGINS env değişkeninden, yoksa localhost
_cors_origins = config(
    'CORS_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:5500,http://127.0.0.1:3000'
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins.split(',') if o.strip()]

# Geliştirme ortamında tüm origin'lere izin ver
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# ── Static & Media ────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise — statik dosyaları sıkıştırır, cache'ler
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Dil & Zaman ───────────────────────────────────────────────
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE     = 'Europe/Istanbul'
USE_I18N      = True
USE_TZ        = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── E-posta ───────────────────────────────────────────────────
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST          = config('EMAIL_HOST',          default='smtp.gmail.com')
EMAIL_PORT          = config('EMAIL_PORT',          default=587, cast=int)
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = config('EMAIL_HOST_USER',     default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL',  default='noreply@serverhub.com')

# ── Güvenlik (sadece production) ──────────────────────────────
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER    = True
    SECURE_CONTENT_TYPE_NOSNIFF  = True
    X_FRAME_OPTIONS               = 'DENY'
    # HTTPS zorunlu kıl (Render HTTPS sağlıyor)
    SECURE_PROXY_SSL_HEADER      = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE        = True
    CSRF_COOKIE_SECURE           = True

# ── Scraper ───────────────────────────────────────────────────
SCRAPE_INTERVAL_MINUTES = 30
SCRAPE_REQUEST_TIMEOUT  = 10
SCRAPE_MAX_RETRIES      = 2
