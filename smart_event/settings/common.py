# Python imports
from os.path import abspath, basename, dirname, join, normpath
from django.contrib import messages
import sys


# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# db routers
DATABASE_ROUTERS = [
    'smart_event.settings.routers.TenantRouter'
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))


# ##### APPLICATION CONFIGURATION #########################

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'apps.acl',
    'apps.dashboard',
    'apps.cliente',
    'apps.core',
    'apps.escala',
    'apps.notification',
    'apps.support',
    'apps.location',
]

# Middlewares
MIDDLEWARE = [
    'smart_event.settings.middleware.multidb_middleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'smart_event.settings.middleware.LocaleMiddleware',
    'smart_event.settings.middleware.TimezoneMiddleware'
]

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
        },
    },
]

# Internationalization
USE_I18N = False


# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    ('Gustavo', 'gustavo.soares.cdc@gmail.com'),
)
MANAGERS = ADMINS

AUTH_USER_MODEL = 'cliente.Client'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# login redirect url
LOGIN_REDIRECT_URL = '/'

# login url
LOGIN_URL = '/acl/login'

# logout redirect urk
LOGOUT_REDIRECT_URL = LOGIN_URL

# ##### DEBUG CONFIGURATION ###############################
DEBUG = False

# ONESIGNAL APP_ID
ONESIGNAL_APP_ID = "ac46fd4e-3813-479a-b175-0149f9789d8f"

# MAPBOX Key
MAPBOX_KEY = 'pk.eyJ1IjoiZ3VzdGF2bzU4NTUiLCJhIjoiY2s0M2R3NnhsMDN0cTNqcWszZGU0YmZtaCJ9.pJWczUcicY45uQZ4IeoKYQ'

# IPSTACK Key
IPSTACK_KEY = 'b23be60d5e84503c80c6fee49a62317e'

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)
