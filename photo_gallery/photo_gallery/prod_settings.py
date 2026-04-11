"""
Django production settings.
Review settings and update them if appropriate.

More information: https://docs.djangoproject.com/en/5.2/topics/settings/
All settings: https://docs.djangoproject.com/en/5.2/ref/settings/
Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

from .database_settings import DB_SETTINGS


def get_list_from_env(env_key):
    """Convert an env variable string/list to a Python list.
  
    Retrieves an env string containing zero, one, or more values 
    separated by commas and returns a list with empty strings removed.
    """
    env_string_list = os.environ.get(env_key, '').split(',')
    return [val for val in env_string_list if val != '']


load_dotenv()  # Load variables from .env in the project root dir

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = get_list_from_env('ALLOWED_HOSTS')

CSRF_COOKIE_SECURE = True  # TODO
CSRF_TRUSTED_ORIGINS = get_list_from_env('CSRF_TRUSTED_ORIGINS')
SESSION_COOKIE_SECURE = True  # TODO
SECURE_SSL_REDIRECT = True  # TODO

INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'imagekit',
    'contact.apps.ContactConfig',
    'nav.apps.NavConfig',
    'photos.apps.PhotosConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photo_gallery.urls'

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
                'photo_gallery.context_processors.global_context',
                'nav.context_processors.navigation',
            ],
        },
    },
]

WSGI_APPLICATION = 'photo_gallery.wsgi.application'

# Database (refer to database_settings.py)
DATABASES = DB_SETTINGS

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# TODO
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'global_static']

# Uploaded & generated files
# https://docs.djangoproject.com/en/5.2/topics/files/
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Emails
# https://docs.djangoproject.com/en/5.2/topics/email/
# TODO
ADMINS = [('Admin1', 'email1@example.com'), ('Admin2', 'email2@example.com')]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'from_email@example.com'
