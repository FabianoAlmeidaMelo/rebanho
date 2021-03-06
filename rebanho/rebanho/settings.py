"""
Django settings for rebanho project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config, Csv
# from dj_database_url import parse as dburl
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')
# SECRET_KEY = 've=gli%pi@)@lbot&_g94ddgyye3)a&lwwamoa6xz5!w4oinfg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
# DEBUG = True

ADMINS = (
    ('Admin Smart Is Cool', 'falmeidamelo@uol.com.br'),
)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

DEFAULT_FROM_EMAIL = u'contato@rebanho.com'


# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'bootstrap3',
    'test_without_migrations',
    'localbr',
    'municipios',
]

LOCAL_APPS = [
    'rebanho.api',
    'rebanho.core',
    'rebanho.propriedades',
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DEFAULT_APPS

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rebanho.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rebanho.wsgi.application'

# ######### CUSTOM USER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'core.User'
# ######### END CUSTOM USER CONFIGURATION

# ######### CUSTOM LOGIN URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = '/login/'
# See: https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/'
# ######### END CUSTOM LOGIN URL CONFIGURATION
LOGOUT_REDIRECT_URL = '/'
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#  ######### DATABASE CONFIGURATION
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#  ######### DATABASE CONFIGURATION
DATABASE_ENGINE = config('DATABASE_ENGINE', default='')
DATABASE_NAME = config('DATABASE_NAME', default='')
DATABASE_USER = config('DATABASE_USER', default='')
DATABASE_PASS = config('DATABASE_PASS', default='')
DATABASE_HOST = config('DATABASE_HOST', default='localhost')
DATABASE_PORT = config('DATABASE_PORT', default='5432')

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASS,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}
#  ######### END DATABASE CONFIGURATION


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL= '/media/'

if DEBUG is False:
    INSTALLED_APPS += ('storages',)
    DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE')  # media file
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    STATICFILES_STORAGE = config('STATICFILES_STORAGE')  # css, js
    # ##
    AWS_S3_CUSTON_DOMAIN = "d12ngo9oha73hw.cloudfront.net"  # CDN
    STATIC_URL = "//%s/staticfile/"  % AWS_S3_CUSTON_DOMAIN
    MEDIA_URL= "//%s/media/"  % AWS_S3_CUSTON_DOMAIN

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')
# Ex  Local: /home/fabiano/projetos/rebanho/rebanho/staticfile

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Ex Local: /home/fabiano/projetos/rebanho/rebanho/media

# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# ######### DEFINE CHILDCRUD UI
CHILDCRUD_UI = 'bootstrap'
# ######### END CHILDCRUD UI