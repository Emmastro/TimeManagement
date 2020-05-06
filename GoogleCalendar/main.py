from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.core.files.storage import Storage
from django.conf import settings

from MainCalendar.eventsData import eventData

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

Storage

class GoogleCalendar:

    def __init__(self, user, courses):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        self.user = user
        self.courses = courses

        if self.user.googleCalendarToken!=None:
                creds = self.user.googleCalendarToken
                print(creds)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_secret = os.path.join(settings.BASE_DIR,'data/client_secret1.json')
               
                flow = InstalledAppFlow.from_client_secrets_file( client_secret, SCOPES)

                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run

            self.user.googleCalendarToken = creds
            self.user.save()
        
        self.service = build('calendar', 'v3', credentials=creds)

    def create(self):

        self.createCalendar()
        self.createEvents()

    def createCalendar(self):
        """ create a new calendar for the student, to separate school events from personal events """
        print("Creating the calendar")
        calendar = {
            'summary': 'ALA Courses',
            'timeZone': 'Africa/Johannesburg',
            }

        self.studentCalendar = self.service.calendars().insert(body=calendar).execute()
        self.user.googleCalendarId = self.studentCalendar['id']
        self.user.save()
    
    def createEvents(self):
        print("Creating Events")

        """
       Color association
       3 Purple
       5 Yellow
       6 Orange
       7 Blue
       8 Grey
       11 Red
       10 Green
       4 Pink
       9 Dark blue
        """
        colors = '8 7 11 5 10 3'.split()
        locations = 'LC1 LC2 LC5 LC10 MST2 LC4'.split()
        
        for block, subject in enumerate(self.courses): #self.user.courses:
            # Go over every subjects
            print(block,subject)
            for i, eventBlock in enumerate(eventData[block]):
                # Go over the reccurent group of the subject
                event = {
                    'summary': subject,
                    'location': locations[block],
                    'description': 'Class description',
                    'start': {
                        'dateTime': eventBlock['start'],
                        'timeZone': 'Africa/Johannesburg',
                    },
                    'end': {
                    'dateTime': eventBlock['end'],
                    'timeZone': 'Africa/Johannesburg',
                    },
                    'recurrence': [
                        'RRULE:' + eventBlock['recurrence']
                    ],
                    'colorId':colors[block],
                }

                event = self.service.events().insert(
                    calendarId=self.studentCalendar['id'], body=event).execute()


        # Save the event id in the database

    def getUserInfo(self):
        """ Returns a preformated json that will be saved in the user's calendar """        
        return None


    def displayEvents(self):

        print('Print 10 events from now')

        now = datetime.datetime.now.isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])