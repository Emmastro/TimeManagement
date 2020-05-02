#import django_heroku
try:
	
	from .local import *

except Exception as e:
	
	from .production_aws import *
