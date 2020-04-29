from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User


class Student(User):
	""""""
	
	course = models.ManyToManyField('MainCalendar.Course')
	googleCalendarToken = models.CharField(max_length = 128)
	microsoftCalendarToken = models.CharField(max_length = 128)

class Teacher(User):

	bio = models.TextField()