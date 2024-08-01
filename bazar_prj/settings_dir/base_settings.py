# -*- coding:utf-8 -*-

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

"""Base settings shared by all environments"""
# if you need to override something do it in local_settings.py

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = False

# https://docs.djangoproject.com/en/2.0/ref/settings/#installed-apps
DJANGO_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'django_filters',
    'versatileimagefield',
    # 'crispy_forms',
    # 'compressor',
    # 'mptt',
    # 'leaflet',
    # 'leaflet_storage',
    # 'djgeojson',
)

COPY_START_YEAR = 2024

MY_APPS = (
    'users',
    'pages',
    'product'
)

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + MY_APPS


# =============================================================================
# Project URLS and media settings
# =============================================================================
# https://docs.djangoproject.com/en/2.0/ref/settings/#root-urlconf.
ROOT_URLCONF = 'bazar_prj.urls'

# URL that handles the media served from MEDIA_ROOT. Use a trailing slash.
# https://docs.djangoproject.com/en/2.0/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL prefix for static files.
# https://docs.djangoproject.com/en/2.0/ref/settings/#static-url
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.join(BASE_DIR, "../", 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, "../", 'mediafiles')

# store your static files in apps "static/" subdirectories and in STATICFILES_DIRS.
# add to urls: urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# and use it like this in your templates {% static "media/your_asset_file" %}
STATICFILES_DIRS = [
    "media", os.path.join(BASE_DIR, "media" ),
    "static", os.path.join(BASE_DIR, "static" )
]
print(BASE_DIR)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
]

# COMPRESS_ENABLED = False

# =============================================================================
# Auth / security
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# =============================================================================

# Password validation
AUTH_PASSWORD_VALIDATORS = [
     { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
     { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
     { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
     { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# =============================================================================
# Templates
# https://docs.djangoproject.com/en/2.0/ref/settings/#templates
# =============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages'      # messaging

                # 'gui.context_processors.navaccount_processor',
                # 'umap.context_processors.settings',  example- free software
            ],
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            'libraries': {
                # Alternatively, template tag modules can be registered through the 'libraries'
                # argument to DjangoTemplates. This is useful if you want to use a different label
                # from the template tag module name when loading template tags. It also enables you
                # to register tags without installing an application.
                # url: https://pypi.org/project/django-copyright/
                'template_tags': 'pages.templatetags.tags_extra',
            },
        },
    },
]

# =============================================================================
# Middleware
# See: https://docs.djangoproject.com/en/2.0/ref/settings/#middleware
# =============================================================================
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',         # (1) This must be first on the list
    'django.middleware.locale.LocaleMiddleware',             # for translation to LANGUAGE_CODE - todo
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # The default message storage backend relies on sessions
    'django.middleware.common.CommonMiddleware',             # (2)
    'django.middleware.csrf.CsrfViewMiddleware',             # cross-site request forgery -
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'       # (3) cache must be in order of (1), (2), (3)
]


# =============================================================================
# LOGGING
# https://docs.djangoproject.com/en/2.0/topics/logging/
# =============================================================================



# =============================================================================
# STORAGE
# =============================================================================

# Django can by default use any cache backend as session backend and you benefit
# from that by using django-redis as backend for session storage without installing
# any additional backends
# systemctl start redis
# redis-cli -n 1
# 127.0.0.1:6379[1]> keys *
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"
# SERIALIZATION_MODULES = {
#     'geojson': 'djgeojson.serializers'
# }
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'  # default

# Configure as cache backend - see prod/dev settings
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

# =============================================================================
# Miscellaneous project settings
# =============================================================================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# =============================================================================
# Third party app settings
# =============================================================================
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True

# leaflet stuff
# LEAFLET_CONFIG = {
#     'RESET_VIEW': False,
# }

# SITE SETTINGS
# https://docs.djangoproject.com/en/2.0/ref/settings/#site-id
SITE_ID = 1
SITE_URL = "https://www.neighborhoodbazar.com"
SITE_NAME = 'Neighborhood Bazar'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'

AUTH_USER_MODEL = "users.CustomUser"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = 'login'
# ENABLE_ACCOUNT_LOGIN = True
# AUTHENTICATION_BACKENDS += ()

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'product_headshot': [
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__100x100'),
        ('medium_square_crop', 'crop__400x400'),
        ('small_square_crop', 'crop__50x50')
    ]
}