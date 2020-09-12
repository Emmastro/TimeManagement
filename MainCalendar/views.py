from django.shortcuts import render

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from Accounts.auth_helper import initialize_context, get_token
from Accounts.models import Student

from .models import*

from MicrosoftCalendar.graph_helper import get_calendars, get_user, get_calendar_events, create_calendar, create_events

import dateutil.parser
from django.conf import settings


class CalendarTemplateView(ListView):

    template_name = 'templates.html'
    model = TimeTableTemplate
    context_object_name = "templates"
    paginate_by = 20
    #order_by="category"


class CreateCalendarTemplate(View):

    template_name = 'newTemplate.html'

    def get(self, request):
        
        try:
            token = get_token(request)
        except:
            return redirect('login')
            
        context = initialize_context(request)
        email = context.get("user").get("email")

        if  email in settings.ADMINS or email.split("@")[1]=="africanleadershipacademy.org" :
            
            context["admin"] = True
        else:
            return redirect("home")

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
            name='Week {}'.format(week))

            #print("Start, End : ", previousCells, cells)
            for cell in range(previousCells, cells):

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
        
        try:
            token = get_token(request)
        except:
            return redirect('login')

        context = initialize_context(request)

        email = context.get("user").get("email")
        if  email in settings.ADMINS or email.split("@")[1]=="africanleadershipacademy.org" :
            
            context["admin"] = True
            
        
        templates = TimeTableTemplate.objects.all()

        # Get the list of calendars from the user
        calendars = get_calendars(token)
        calendarNames = []

        for c in calendars:
            calendarNames.append(c['name'])
        
        context['calendarNames'] = calendarNames
        context['templates'] = templates
        #print(context)
        
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

        #blocks =  [b[0] for b in Block.BLOCKS.choices]
        
        #** Get the activities from the form
        blocks = [
            request.POST['blue'],
            request.POST['red'],
            request.POST['yellow'],
            request.POST['green'],
            request.POST['grey'],
            request.POST['purple'],
            request.POST['black'],
            request.POST['orange'],
            "Breakfast",
            "Flex",
            "Lunch",
            "Dinner",
            request.POST['sport'],
            "Clubs and societies",
            request.POST['research-extra-curricular']],
            
        #print("Blocks:", blocks[0])
        events = create_events(
            token=token,
            calendarId=calendarId,
            blocks=blocks[0],
            startDate = request.POST['start'],
            endDate = request.POST['end'],
            template = request.POST['templates'])

        

        return render(request, self.template_name, locals())
        

def privacy(request):

    return render(request, 'privacy.html')

def termsConditions(request):

    return render(request, 'termsConditions.html')