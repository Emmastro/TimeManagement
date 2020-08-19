from django.db import models

# Create your models here.


class TimeTableTemplate(models.Model):

	name = models.CharField(max_length=128)
	cycle = models.SmallIntegerField()
	timeInterval = models.SmallIntegerField()
	start = models.TimeField()
	end = models.TimeField()


class Block(models.Model):

	BLOCKS = models.TextChoices('Block', "Grey Blue Red Yellow Green Purple Sport Extra-Curricular ")
	start = models.TimeField()
	end = models.TimeField()
	block = models.CharField(choices = BLOCKS.choices, max_length=20)