from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MainCalendar.models import Course, Subject

import os
import json
from Account.models import Teacher

class Command(BaseCommand):

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR,'MainCalendar/management/data/Subjects.json')) as f:
            subjects = json.load(f)

        for subject in subjects:
            teacher = Teacher.objects.get_or_create(username=subject['teacher'])

            Subject.objects.get_or_create(title=subject['title'], teacher=teacher[0])[0].save()