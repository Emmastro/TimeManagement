from django.urls import path
from . import views


urlpatterns = [
	
	path('', views.Home_view.as_view(), name='home'),

]
