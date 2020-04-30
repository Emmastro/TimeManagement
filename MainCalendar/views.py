from django.shortcuts import render

# Create your views here.
from django.views import View

from django.utils.decorators import method_decorator

from Account.models import Student
from django.contrib.auth.decorators import login_required
from .models import*

@method_decorator(login_required, name='dispatch')
class Home_view(View):
    
    model = Student
    template_name = "main.html"
    
    
    def get(self, request, *args, **kwargs):
        
        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        subjects = Subject.objects.all()
        return render(request, self.template_name, locals())
        
    def post(self, request, *args, **kwargs):
        """ Save or update events on the calendar"""
        blocks = 'Grey Blue Red Yellow Green Purple'.split()
        subjects = Subject.objects.all()
        
        blocks = [request.POST['Grey'],request.POST['Blue'],request.POST['Red'],request.POST['Yellow'],request.POST['Green'],request.POST['Purple']]
        
        self.populateEvents(blocks, request.user)
        return render(request, self.template_name, locals())
        
    def populateEvents(self, blocks):
        """ Populate courses in the user's calendar"""


        pass