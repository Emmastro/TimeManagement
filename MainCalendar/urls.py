from django.urls import path
from . import views


urlpatterns = [
	path('courses', views.CoursesView.as_view(), name='courses'),
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
