from django.shortcuts import render

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from Accounts.auth_helper import initialize_context, get_token
from Accounts.models import Student

from .models import*

from MicrosoftCalendar.graph_helper import get_calendars, get_user, get_calendar_events, create_calendar, create_events

import dateutil.parser


class CalendarTemplateView(ListView):

    template_name = 'templates.html'
    model = TimeTableTemplate
    context_object_name = "templates"
    paginate_by = 20
    #order_by="category"


class CreateCalendarTemplate(View):

    template_name = 'newTemplate.html'

    def get(self, request):
        
        #context = initialize_context(request)

        # TODO: JS duplicate calendar for different time cycles
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        
        # TODO: Using the data saved as a calendar template for students
        context = {}
        data = request.POST
        templateName = data['template-name']
        timeInterval = int(data['time-interval'])
        startTime = data['start-time']
        endTime = data['end-time']
        cycle = int(data['cycle']) # The model storing the schedule should be ManyToMany
        
        timeTableTemplate = TimeTableTemplate.objects.create(
            name=templateName,
            interval=timeInterval,
            start=startTime,
            end=endTime
        )
        previousCells = 0

        for week in range(cycle): # Go through week A, B, and any other week cycle
           
            cells = int(data['cells{}'.format(week)])
            weekTemplate = WeekTemplate.objects.create(
            name='Week {}'.format(cycle))

            print("Start, End : ", previousCells, cells)
            for cell in range(previousCells, cells):

                
                # Save each cell. Will consider merging cells when rendering the template on a calendar

                cell = Cell.objects.create(color=data['cell{}'.format(cell)])

                weekTemplate.cells.add(cell)

            previousCells+=cells
            weekTemplate.save()
            timeTableTemplate.weeks.add(weekTemplate)
        
        timeTableTemplate.save()

        return render(request, self.template_name, context)


class DashboardView(View):

    def get(self, request):
        context = initialize_context(request)
        
        return render(request, self.template_name, context)

class SetupCalendarView(View):

    template_name = 'setupCalendar.html'

    def get(self, request, *args, **kwargs):
        
        context = initialize_context(request)
        templates = TimeTableTemplate.objects.all()
        token = get_token(request)
        # Get the list of calendars from the user
        calendars = get_calendars(token)
        calendarNames = []

        for c in calendars:
            calendarNames.append(c['name'])
        
        context['calendarNames'] = calendarNames
        context['templates'] = templates
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """ Get or Create a calendar and add the activities/events on it"""

        token = get_token(request)
        form_calendarId = int(request.POST['calendar'])

        # Create a calendar using the title from the form
        if form_calendarId == 0:
            calendarId = create_calendar(token=token, name = request.POST['calendar-name'])
        
        else: # Get the calendar selected
            calendar = get_calendars(token=token)[form_calendarId-1]
            calendarId = calendar['id']

        # Add activities/events

        #** Get the blocks from the form (labels of each input)

        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        
        #** Get the activities from the form
        courses = [
            request.POST['grey'],
            request.POST['blue'],
            request.POST['red'],
            request.POST['yellow'],
            request.POST['green'],
            request.POST['purple']]

        events = create_events(
            token=token,
            calendarId=calendarId,
            courses=courses,
            startDate = request.POST['start'],
            endDate = request.POST['end'],
            template = request.POST['templates'])

        return render(request, self.template_name, locals())
        

def privacy(request):

    return render(request, 'privacy.html')

def termsConditions(request):

    return render(request, 'termsConditions.html')