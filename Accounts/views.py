from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView, CreateView
from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required


from .models import *
from django.contrib.auth.forms import AuthenticationForm


class Login(LoginView):

    form_class = AuthenticationForm
    template_name = "login.html"
    redirect_field_name = "redirect"

class LostPassword(View):

    page_title = "New password"
    form_class = AuthenticationForm
    template_name = "loginpage.html"


def logout_view(request):

    logout(request)

    return redirect('home')

  
def account_redirect(request):
    
    return redirect('accounts', request.user.id)

@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    """Update the user's details"""

    template_name = "account.html"
    model = Student
    #form_class = StudentForm

    def __init__(self, *args, **kwargs):
        super(UpdateView, self).__init__(*args, **kwargs)
        self.context_object_name = 'Student'