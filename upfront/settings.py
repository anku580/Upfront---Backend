
"""
Django settings for upfront project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.conf import settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*7l@_fegt809_c*e9xc)_c@dqxfc0)-yijeg2+5d)*s*c)7%32'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'paypal.standard.ipn',
    'myuser',
    'menu_app',
    'restaurant_app',
    'orders',
    'temperorycart',
    'payment',
    'addons_app',
    'referrals',
    'tablebooking_app',
    'favourites',
    'customization_app',
    'rating_app',

]

AUTH_USER_MODEL = 'myuser.MyUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'upfront.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': ['templates'],

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

WSGI_APPLICATION = 'upfront.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'upfront',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'myuser.backends.JWTAuthentication',
    ),

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),

    'EXCEPTION_HANDLER': 'myuser.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
     'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}





STATIC_URL = '/static/'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


#django-paypal settingd
PAYPAL_RECEIVER_EMAIL = 'diastomjose@gmail.com'
PAYPAL_TEST='True'

MEDIA_URL = '/media/'

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@sandbox221a1db8408a4ac19bc03938cb5873f1.mailgun.org'
EMAIL_HOST_PASSWORD = '31ac31387191624fc058673425999aaa-de7062c6-1d40a4f4'
EMAIL_USE_TLS = True
