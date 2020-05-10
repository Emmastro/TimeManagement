import os
import dj_database_url
import django_heroku
from django.core.wsgi import get_wsgi_application
from .base import*


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Connect to production database
HOSTED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ALATIME',
        'USER': 'emmamurairi',
        'PASSWORD': 'thisismypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

import dj_database_url

db_from_env  = dj_database_url.config(conn_max_age=600, ssl_require=True)

DATABASES['default'].update(db_from_env)

CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = False
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False

django_heroku.settings(locals())


DEBUG = True