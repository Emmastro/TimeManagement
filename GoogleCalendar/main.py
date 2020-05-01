from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.core.files.storage import Storage
from django.conf import settings

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

Storage

class GoogleCalendar:

    def __init__(self, user):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        self.user = user

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
        
        # data[COLOR_ID][RECURENCE_CAT_ID][PROPERTY]
        data = [
        # Grey Block 0
        [
            # Week A 1
            {
                'start':'2020-09-07T08:00:00-00:00',
                'end': '2020-09-07T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 2
            {
                'start':'2020-09-08T11:00:00-00:00',
                'end': '2020-09-08T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A* 3
            {
                'start':'2020-09-26T09:00:00-00:00',
                'end': '2020-09-26T10:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 4
            {
                'start':'2020-09-14T13:15:00-00:00',
                'end': '2020-09-14T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SU,WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 5
            {
                'start':'2020-09-16T09:00:00-00:00',
                'end': '2020-09-16T10:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
           
        ],
        # Blue block 1
        [
            # Week A 6
            {
                'start':'2020-09-07T09:00:00-00:00',
                'end': '2020-09-07T10:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 7
            {
                'start':'2020-09-08T13:15:00-00:00',
                'end': '2020-09-08T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 8
            {
                'start':'2020-09-11T13:30:00-00:00',
                'end': '2020-09-11T14:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A* 9
            {
                'start':'2020-09-26T10:00:00-00:00',
                'end': '2020-09-26T11:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 10
            {
                'start':'2020-09-15T08:00:00-00:00',
                'end': '2020-09-15T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 11
            {
                'start':'2020-09-16T11:00:00-00:00',
                'end': '2020-09-16T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
        ],
        # Red Block 2
        [  
            # Week A 12
            {
                'start':'2020-09-07T11:00:00-00:00',
                'end': '2020-09-07T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 13
            {
                'start':'2020-09-09T08:00:00-00:00',
                'end': '2020-09-09T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 14
            {
                'start':'2020-09-10T11:30:00-00:00',
                'end': '2020-09-10T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 15
            {
                'start':'2020-09-07T14:30:00-00:00',
                'end': '2020-09-07T15:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A* 16
            {
                'start':'2020-09-26T11:30:00-00:00',
                'end': '2020-09-26T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 17
            {
                'start':'2020-09-15T09:00:00-00:00',
                'end': '2020-09-15T10:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 18
            {
                'start':'2020-09-16T13:15:00-00:00',
                'end': '2020-09-16T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
        ],
        # Yellow Block
        [
            # Week A 19
            {
                'start':'2020-09-07T13:15:00-00:00',
                'end': '2020-09-07T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 20
            {
                'start':'2020-09-09T09:00:00-00:00',
                'end': '2020-09-09T10:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 21
            {
                'start':'2020-09-12T09:00:00-00:00',
                'end': '2020-09-12T10:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 22
            {
                'start':'2020-09-14T08:00:00-00:00',
                'end': '2020-09-17T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 23
            {
                'start':'2020-09-15T11:00:00-00:00',
                'end': '2020-09-15T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
        ],
        # Green block
        [
            # Week A 24

            {
                'start':'2020-09-08T08:00:00-00:00',
                'end': '2020-09-08T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 25
            {
                'start':'2020-09-16T11:00:00-00:00',
                'end': '2020-09-16T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 26
            {
                'start':'2020-09-12T10:00:00-00:00',
                'end': '2020-09-12T11:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 27
            {
                'start':'2020-09-14T09:00:00-00:00',
                'end': '2020-09-14T10:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 28
            {
                'start':'2020-09-15T13:15:00-00:00',
                'end': '2020-09-15T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 29
            {
                'start':'2020-09-18T13:30:00-00:00',
                'end': '2020-09-18T14:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
        ],
        # Purple Block
        [
            # Week A 30
            {
                'start':'2020-09-08T09:00:00-00:00',
                'end': '2020-09-08T10:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 31
            {
                'start':'2020-09-09T13:15:00-00:00',
                'end': '2020-09-09T14:15:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week A 32
            {
                'start':'2020-09-12T11:30:00-00:00',
                'end': '2020-09-12T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4;UNTIL=20210530T220000Z'
            },
            # Week B 33
            {
                'start':'2020-09-14T11:00:00-00:00',
                'end': '2020-09-14T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=MO;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 34
            {
                'start':'2020-09-16T08:00:00-00:00',
                'end': '2020-09-16T09:00:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 35
            {
                'start':'2020-09-17T11:30:00-00:00',
                'end': '2020-09-17T12:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=TH;INTERVAL=2;UNTIL=20210530T220000Z'
            },
            # Week B 36
            {
                'start':'2020-09-18T14:30:00-00:00',
                'end': '2020-09-18T15:30:00-00:00',
                'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2;UNTIL=20210530T220000Z'
            },
        ]    
    ]

        #data: [block][blockGroup]

        colors = '#808080 #0000FF #FF0000  #FFFF00 #008000 #800080'.split()

        for block, subject in enumerate('French CS Afr_Stud Math WR EL'.split()): #self.user.courses:
            # Go over every subjects
            for i, eventBlock in enumerate(data[block]):
                # Go over the reccurent group of the subject
                event = {
                    'summary': subject,
                    'location': 'LC4',
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
                    'colorId':str(block),
                }
                print(block, i)

                event = self.service.events().insert(calendarId=self.studentCalendar['id'], body=event).execute()
            
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
