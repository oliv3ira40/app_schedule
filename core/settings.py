"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from distutils.util import strtobool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0bo4u+pq71(n2+%!@6w2f3tb#$^!j)@c0jmrg1$!rsi#*1(*m7'

# Caminho para o arquivo .env (geralmente na raiz do projeto)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv('DEBUG', 'False'))

# Ativa a Sentry apenas em produção
production = strtobool(os.getenv('PRODUCTION', 'False'))
if production:
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://74a13cc1100353ca54fa4319d88967ec@o4508072935292928.ingest.us.sentry.io/4508072939880448",
        traces_sample_rate=1.0,
        environment="prod",
        profiles_sample_rate=1.0,
    )

ALLOWED_HOSTS = ['127.0.0.1', 'flexibook.com.br', 'www.flexibook.com.br']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Para permitir cookies seguros e compatibilidade com proxies
CSRF_TRUSTED_ORIGINS = ['https://flexibook.com.br']

# Se você estiver usando SSL
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Para o uso de proxies reversos como Nginx ou Cloudflare
USE_X_FORWARDED_HOST = True

# Application definition
INSTALLED_APPS = [
    # 'jazzmin',

    "admin_interface",
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'person',
    'schedule',
    'website',
    'finances',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JAZZMIN_SETTINGS = {
#     "show_ui_builder": True,
#     'changeform_format_overrides': {
#         'entity.Workday': 'single'
#     },
#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users",
#         "entity.Entity": "fas fa-list",
#         "entity.Person": "fas fa-list",
#         "entity.ServiceProvided": "fas fa-list",
#         "entity.Workday": "fas fa-list",
#         "entity.TypeEntity": "fas fa-list",
#         "entity.Schedule": "fas fa-list",
#         "entity.DayOfWeek": "fas fa-list",
#     },
# }

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": True,
#     "brand_small_text": False,
#     "brand_colour": "navbar-white",
#     "accent": "accent-navy",
#     "navbar": "navbar-white navbar-light",
#     "no_navbar_border": False,
#     "navbar_fixed": False,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": True,
#     "sidebar": "sidebar-light-navy",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": True,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": False,
#     "theme": "minty",
#     # "theme": "materia",
#     # "theme": "sandstone",
#     "dark_mode_theme": None,
#     "button_classes": {
#         "primary": "btn-outline-primary",
#         "secondary": "btn-outline-secondary",
#         "info": "btn-outline-info",
#         "warning": "btn-outline-warning",
#         "danger": "btn-outline-danger",
#         "success": "btn-outline-success"
#     },
#     "actions_sticky_top": False
# }

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": True,
#     "brand_small_text": False,
#     "brand_colour": "navbar-dark",
#     "accent": "accent-info",
#     "navbar": "navbar-dark",
#     "no_navbar_border": False,
#     "navbar_fixed": False,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": True,
#     "sidebar": "sidebar-dark-info",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": True,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": False,
#     "theme": "solar",
#     "dark_mode_theme": None,
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-outline-info",
#         "warning": "btn-outline-warning",
#         "danger": "btn-outline-danger",
#         "success": "btn-outline-success"
#     },
#     "actions_sticky_top": False
# }

# Django unfold settings
from admin_interface.theme_settings import *
