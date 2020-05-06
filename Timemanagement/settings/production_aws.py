from .base import *
import os
import dj_database_url
from .base import*

ALLOWED_HOSTS = ['54.208.156.24']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}


"""
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
 'NAME': 'djangostack',
'HOST': '/opt/bitnami/postgresql',
'PORT': '5432',
 'USER': 'bitnami',
 'PASSWORD': '2425de1e84'
}
}
"""