from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MainCalendar.models import Course, Subject
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR,'MainCalendar/management/data/Subjects.json')) as f:
            subjects = json.load(f)

        for subject in subjects:
            Subject.objects.create(title=subject['title'], teacher=subject['teacher'], bio="Demo").save()