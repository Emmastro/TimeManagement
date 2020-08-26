from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Cell)
admin.site.register(TimeTableTemplate)
admin.site.register(WeekTemplate)
admin.site.register(Block)