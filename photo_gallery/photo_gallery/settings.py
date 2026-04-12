"""
Django development settings.
These settings are not suitable for a live/production site!
Refer to `prod_settings.py` and deployment documentation for more details.

More information: https://docs.djangoproject.com/en/5.2/topics/settings/
All settings: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

from .database_settings import *
from .email_settings import *


def get_bool_from_env(env_key, default_val=None):
    """Convert an env variable Boolean string to a Python Boolean.
    
    Optionally provide a default value to use (str: 'True' or 'False') 
    if the environment variable hasn't been set.
    """
    try:
        env_string_lower = os.environ.get(env_key, default_val).lower()
    except AttributeError:
        raise AssertionError('You must set the environment variable or ' \
        'pass a default value string (True/False)')
    
    if not (env_string_lower == 'true' or env_string_lower == 'false'):
        raise AssertionError('The value must be a Boolean (True/False)')
    
    return env_string_lower == 'true'


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
DEBUG = True

# Security
# https://docs.djangoproject.com/en/5.2/topics/security/
ALLOWED_HOSTS = get_list_from_env('ALLOWED_HOSTS')

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
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
TIME_ZONE = os.environ.get('TIME_ZONE')
USE_I18N = get_bool_from_env('USE_I18N', 'True')
USE_TZ = get_bool_from_env('USE_TZ', 'True')

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
