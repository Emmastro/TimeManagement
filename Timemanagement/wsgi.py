import os
from django.core.wsgi import get_wsgi_application

import sys

# Server configuration for AWS Hosting
sys.path.append('/opt/bitnami/apps/django/django_projects/TimeManagement')

os.environ.setdefault(
    "PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/TimeManagement/egg_cache"
    )

# Django setting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Timemanagement.settings')

application = get_wsgi_application()
