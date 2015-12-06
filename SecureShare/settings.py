"""
Django settings for SecureShare project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '11*f6!@du+=p=sv671@0+vh#r#n&*v!xcgq*(6grlezua_-v)('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'master',
    'reports',
    'post',
    'rest_framework',
    'tinymce',
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)
TINYMCE_JS_URL = os.path.join(MEDIA_ROOT, "js/tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, "js/tiny_mce")
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'simple',
    'relative_urls': False,
    'plugins': 'media',
    'theme_advanced_buttons1': 'bold,italic,underline,bullist,numlist,|,media,link,unlink,image',
    'theme_advanced_resizing': True,
    'theme_advanced_path': False,
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_HOST_USER = 'secureshare21uva@yahoo.com'
EMAIL_HOST_PASSWORD = 'mygleeclubisafireman'
EMAIL_PORT = 465
#EMAIL_USE_TLS = True
EMAIL_USE_SSL = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'SecureShare.urls'

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

WSGI_APPLICATION = 'SecureShare.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

WSGI_APPLICATION = 'SecureShare.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
