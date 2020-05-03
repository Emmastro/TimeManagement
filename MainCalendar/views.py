from django.shortcuts import render

from django.views import View

from django.utils.decorators import method_decorator

from Accounts.auth_helper import initialize_context
from Accounts.models import Student
from django.contrib.auth.decorators import login_required
from .models import*
from GoogleCalendar.main import GoogleCalendar

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from MicrosoftCalendar.graph_helper import get_user, get_calendar_events
import dateutil.parser



def home(request):
  context = initialize_context(request)

  return render(request, 'home.html', context)


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
        
        courses = [
            request.POST['Grey'],
            request.POST['Blue'],
            request.POST['Red'],
            request.POST['Yellow'],
            request.POST['Green'],
            request.POST['Purple']]
        print(courses)
        google = False
        microsoft = True

        if google:
            calendar = GoogleCalendar(
                user=Student.objects.get(username="Demo00"),#pk=request.user.id),
                courses=courses
                )
            calendar.create()
        elif microsoft:
            pass

        return render(request, self.template_name, locals())
        

def privacy(request):

    return render(request, 'privacy.html')

def termsConditions(request):

    return render(request, 'termsConditions.html')