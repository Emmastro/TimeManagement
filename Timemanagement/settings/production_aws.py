from .base import *
import os
import dj_database_url
from .base import*

ALLOWED_HOSTS = ['3.223.180.215']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'timemanagement',
    'HOST': 'ls-da52e14c356faa9756bf02bb29eaa12c26d02480.cc2syslbeiea.us-east-1.rds.amazonaws.com',
    'PORT': '5432',
    'USER': 'dbmasteruser',
    'PASSWORD': '4lB<B%9e!V&0U~Hl*EP]z];Q2HBEY!E7'
    }
}