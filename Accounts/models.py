from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

class Student(User):
	""""""
	
	course = models.ManyToManyField('MainCalendar.Course')
	googleCalendarToken = PickledObjectField(null=True)
	microsoftCalendarToken = models.CharField(max_length = 128)

class Teacher(User):

	bio = models.TextField()