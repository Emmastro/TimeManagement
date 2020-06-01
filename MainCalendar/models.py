from django.db import models

# Create your models here.
class Course(models.Model):
	""" Consider the subject and the block """

	COLORS = models.TextChoices('Block', "Grey Blue Red Yellow Green Purple Sport Extra-Curricular ")
	subject = models.ForeignKey('MainCalendar.Activity', on_delete=models.CASCADE)
	block = models.CharField(choices = COLORS.choices, max_length=20)

class Activity(models.Model):

	title = models.CharField(max_length = 128)
	description = models.TextField()

class Schedule(models.Model):
	""" Can be a term, or any custom period"""

	title = models.CharField(max_length=128)
	calendarId = models.CharField(max_length=125)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	activities = models.ManyToManyField('MainCalendar.Activity')

