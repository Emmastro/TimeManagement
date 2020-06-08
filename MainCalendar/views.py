from django.shortcuts import render

from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator

from Accounts.auth_helper import initialize_context, get_token
from Accounts.models import Student
from django.contrib.auth.decorators import login_required
from .models import*
from GoogleCalendar.main import GoogleCalendar

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from MicrosoftCalendar.graph_helper import get_calendars, get_user, get_calendar_events, create_calendar, create_events
import dateutil.parser



class DashboardView(View):

    template_name = 'student_dashboard.html'
    

    def get(self, request):
        
        return render(request, self.template_name, locals())

class CalendarActivitiesView(View):

    template_name = 'calendar_activities.html'

    def get(self, request, *args, **kwargs):
        
        token = get_token(request)
        # Get the list of calendars from the user
        calendars = get_calendars(token)
        calendarNames = []

        for c in calendars:
            calendarNames.append(c['name'])
        
        print(calendarNames)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        """ Get or Create a calendar and add the activities/events on it"""

        token = get_token(request)

        # Get or create calendar
        
        calendarId = create_calendar(token=token)
        #**Implement Getting an existing calendar

        # Add activities/events
        #** Get the blocks from the form        
        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        
        #** Get the activities from the form
        courses = [
            request.POST['Grey'],
            request.POST['Blue'],
            request.POST['Red'],
            request.POST['Yellow'],
            request.POST['Green'],
            request.POST['Purple']]
        #** The UI should allow to add more activities/events before submiting, and choose the event color
        """if google:
            calendar = GoogleCalendar(
                user=Student.objects.get(username="Demo00"),#pk=request.user.id),
                courses=courses
                )
            calendar.create()"""
        events = create_events(token=token, calendarId=calendarId, courses=courses)

        return render(request, "success.html", locals())
        

def privacy(request):

    return render(request, 'privacy.html')

def termsConditions(request):

    return render(request, 'termsConditions.html')