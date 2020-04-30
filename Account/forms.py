from django.contrib.auth.forms import  UserCreationForm
from django import forms
from .models import Student

from django import forms




class User_ALAMAUForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'email', )
    