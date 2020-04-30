from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from Account.models import Student, Teacher
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = [Student, Teacher]

        for l in range(2):

            for i in range(10):
                
                user = users[l](username='Demo{}{}'.format(i,l))
                
                user.set_password("Demo")

                user.save()