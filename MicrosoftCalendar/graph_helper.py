from requests_oauthlib import OAuth2Session
from MainCalendar.eventsData import eventData

graph_url = 'https://graph.microsoft.com/v1.0'
headers = {"Content-Type": "application/json"}

def get_user(token):
  graph_client = OAuth2Session(token=token)

  user = graph_client.get('{0}/me'.format(graph_url))

  return user.json()


def get_calendar_events(token):
  graph_client = OAuth2Session(token=token)

  query_params = {
    '$select': 'subject,organizer,start,end',
    '$orderby': 'createdDateTime DESC'
  }

  events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)

  return events.json()

def create_calendar(token):
  
  calendarId=None

  graph_client = OAuth2Session(token=token)
  query_params = {
        'name':'My courses'
    }
    
  calendar = graph_client.post(
      '{0}/me/calendars'.format(graph_url),
      json=query_params,
      headers=headers)

  try:
    calendarId = calendar.json()['id']
  except:
    pass
  return calendarId

def bydayConvert(value):

  if ',' in value:
    BYDAY = list(value.split(','))
  else:
    BYDAY = [value]

  days = []

  for day in BYDAY:
    # Map the abreviated day version to the full day
    for fullday in 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split():
      if day.lower() == fullday[:2].lower():
        days.append(fullday)

  return days 

def rruleToMSRecurrence(rrule, startDate):
  """ convert recurrence statement from rrule formate to the Microsoft calendar format"""

  #FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2;UNTIL=20210530T220000Z
  #FREQ, BYDAY, INTERVAL = 0,0,0

  data = {}
  for l in rrule[:-23].split(';'):
    var, value = l.split('=')
    data.update({var:value})

  data['BYDAY'] = bydayConvert(data['BYDAY'])

  recurrence = {
    "recurrence": {
    "pattern": {
      "type": data['FREQ'].lower(),
      "interval": data['INTERVAL'],
      "daysOfWeek": data['BYDAY'],
      #"index": "first"
    },
    "range": {
      "type": "endDate",
      "startDate": startDate[:10],
      "endDate": "2021-06-01"
    }
    }
  }

  
  return recurrence

def create_events(token, calendarId, courses):
  

  colors = 'Gray Blue Red Yellow Green Purple'.split()
  locations = 'LC1 LC2 LC5 LC10 MST2 LC4'.split()
  
  graph_client = OAuth2Session(token=token)


  for block, subject in enumerate(courses): #self.user.courses:
  # Go over every subjects

      for i, eventBlock in enumerate(eventData[block]):
        # Go over the reccurent group of the subject

          event = {
              'Subject': subject,
              'Location':{
                'displayName':locations[block]
                } ,
              "Body": {
                "ContentType": "HTML",
                "Content": "This is the course description"
                },
              'start': {
                  'dateTime': eventBlock['start'],
                  'timeZone': 'Africa/Johannesburg',
              },
              'end': {
              'dateTime': eventBlock['end'],
              'timeZone': 'Africa/Johannesburg',
              },
              'categories': ['{} category'.format(colors[block])],
              'recurrence': rruleToMSRecurrence(eventBlock['recurrence'], eventBlock['start'])['recurrence']
              #'colorId':colors[block],
          }
          eventResponse = graph_client.post(
            '{0}//me/calendars/{1}/events'.format(graph_url,calendarId),
            json=event,
            headers=headers)
          print(eventResponse)