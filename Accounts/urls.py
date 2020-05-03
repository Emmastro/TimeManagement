from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import django.contrib

#print(django.contrib.auth.urls.)

urlpatterns = [
	path('login/', views.sign_in, name='login'),
	path('logout/', views.sign_out, name='logout'),
	path('callback/', views.callback, name='callback'),
]