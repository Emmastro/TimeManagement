from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('courses', views.CoursesView.as_view(), name='courses'),
	#path('', views.Home_view.as_view(), name='home'),
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
