from django.urls import path
from . import views


urlpatterns = [
	path('setup-calendar', views.SetupCalendarView.as_view(), name='setupCalendar'),
	path('templates', views.CalendarTemplateView.as_view(), name='templateView'),
	path('templates/new', views.CreateCalendarTemplate.as_view(), name='createCalendarTemplate'),
	#path('dashboard/period/<str:period>', views.CalendarActivitiesView.as_view(), name='period'),
	#path('dashboard/period-form', views.CalendarActivitiesFormView.as_view(), name='period-form'),
	
	path('privacy', views.privacy),
	path('terms-conditions', views.termsConditions)

]
