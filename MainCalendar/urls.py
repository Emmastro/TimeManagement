from django.urls import path
from . import views


urlpatterns = [
	path('dashboard', views.DashboardView.as_view(), name='dashboard'),
	path('dashboard/period/<str:period>', views.PeriodView.as_view(), name='period'),
	path('dashboard/period/save-schedule', views.SaveCalendar.as_view(), name='save-schedule'),
	path('dashboard/period/save-period', views.SaveActivities.as_view(), name='save-period'),
	path('courses', views.CoursesView.as_view(), name='courses'),
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
