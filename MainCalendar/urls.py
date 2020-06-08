from django.urls import path
from . import views


urlpatterns = [
	path('dashboard', views.DashboardView.as_view(), name='dashboard'),
	path('dashboard/period/<str:period>', views.CalendarActivitiesView.as_view(), name='period'),
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
