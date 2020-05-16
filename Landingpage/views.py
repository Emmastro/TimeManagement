from django.shortcuts import render
from Accounts.auth_helper import initialize_context

# Create your views here.

def home(request):

  context = initialize_context(request)
  
  return render(request, 'home.html', context)
