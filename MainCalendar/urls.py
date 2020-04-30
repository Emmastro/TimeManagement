from django.urls import path
from . import views


urlpatterns = [
	
	path('', views.Home_view.as_view(), name='home'),
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
