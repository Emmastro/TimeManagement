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

    template_name = 'admin_.html'
    

    def get(self, request):
        
        token = get_token(request)
        # Get the list of calendars from the user
        calendars = get_calendars(token)
        return render(request, self.template_name)

class PeriodView(View):

    template_name = 'period_.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

class SaveCalendar(View):
    # A calendar can be a term, or any timeframe with coherent activities

    # Check if a calendar with this name does not exist

    # Create the calendar

    # Save the transaction on the database?
    model = None
    fields = None

class UpdateCalendar(View):

    # Get the Calendar

    # Update the calendar
    model = None
    fields = None
    

class SaveActivities(View):

    # Get the Calendar where these activities should be input

    # Save the new activities on the calendar

    # Save the transaction on the database?
    model = None
    fields = None
    
class UpdateActivities(View):

    # Check if there is already some events claching with the new events

    model = None
    fields = None


class CoursesView(View):
    
    model = Student
    template_name = "courses.html"
    
    def get(self, request, *args, **kwargs):
        
        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        subjects = Subject.objects.all()
        return render(request, self.template_name, locals())
        
    def post(self, request, *args, **kwargs):
        """ Save or update events on the calendar"""
        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        subjects = Subject.objects.all()
        token = get_token(request)

        courses = [
            request.POST['Grey'],
            request.POST['Blue'],
            request.POST['Red'],
            request.POST['Yellow'],
            request.POST['Green'],
            request.POST['Purple']]

        google = False
        microsoft = True

        if google:
            calendar = GoogleCalendar(
                user=Student.objects.get(username="Demo00"),#pk=request.user.id),
                courses=courses
                )
            calendar.create()
        elif microsoft:
            calendarId = create_calendar(token=token)
            events = create_events(token=token, calendarId=calendarId, courses=courses)

        return render(request, "success.html", locals())
        

def privacy(request):

    return render(request, 'privacy.html')

def termsConditions(request):

    return render(request, 'termsConditions.html')