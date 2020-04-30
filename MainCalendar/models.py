from django.db import models

# Create your models here.
class Course(models.Model):
	""" Consider the subject and the block """

	COLORS = models.TextChoices('Color', "Grey Blue Red Yellow Green Purple")
	subject = models.ForeignKey('MainCalendar.Subject', on_delete=models.CASCADE)
	block = models.CharField(choices = COLORS.choices, max_length=20)

class Subject(models.Model):

	title = models.CharField(max_length = 128)
	teacher = models.ForeignKey('Accounts.Teacher', on_delete=models.CASCADE)
	description = models.TextField()