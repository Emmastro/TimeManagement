from django.shortcuts import render

# Create your views here.
from django.views import View

from django.utils.decorators import method_decorator

from Account.models import Student


#@method_decorator(login_required, name='dispatch')
class Home_view(View):
    
    model = Student
    template_name = "main.html"
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, locals())
        
    def get_queryset(self):
        """Filter queries"""
        
        pass
        
    def get_context_data(self, **kwargs):
        
        context = super(Home_view, self).get_context_data(**kwargs)
        return context