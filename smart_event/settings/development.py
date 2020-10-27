# Python imports
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
LOGIN_URL = '/acl/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/acl/login'


# ##### DATABASE CONFIGURATION ############################
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smart_event',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    'teste2': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'teste2',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    'teste': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'teste',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS
