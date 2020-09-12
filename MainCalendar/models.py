from django.db import models

# Create your models here.


class Block(models.Model):

	COLORS = "Grey Blue Red Yellow Green Purple Black Orange Pink Pink Orange Orange"
	BLOCKS = models.TextChoices('Block', "Grey Blue Red Yellow Green Purple Black Orange Sport Extra-Curricular Breakfast Lunch")
	
	start = models.TimeField()
	end = models.TimeField()
	block = models.CharField(choices = BLOCKS.choices, max_length=20)


class WeekTemplate(models.Model):

	# Name of the week (Week A, B, A*, ...)
	name = models.CharField(max_length = 20) 

	# Each Cell in that week (with the time interval set from the TimeTableTemplate)
	cells = models.ManyToManyField('Cell') 

	def __str__(self):
		return self.name
	

class TimeTableTemplate(models.Model):

	name = models.CharField(max_length=128)
	interval = models.SmallIntegerField()
	start = models.TimeField()
	end = models.TimeField()
	weeks = models.ManyToManyField('WeekTemplate') #Allow a time table to have multiple week cycles

	def __str__(self):
		return self.name
	

class Cell(models.Model):

	color = models.SmallIntegerField()
	
	