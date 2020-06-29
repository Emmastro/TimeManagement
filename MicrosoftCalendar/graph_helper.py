from requests_oauthlib import OAuth2Session
from MainCalendar.eventsData import eventData

graph_url = 'https://graph.microsoft.com/v1.0'
headers = {"Content-Type": "application/json"}

def get_user(token):
  graph_client = OAuth2Session(token=token)

  user = graph_client.get('{0}/me'.format(graph_url))

  return user.json()

def get_calendars(token):

  graph_client = OAuth2Session(token=token)

  query_params = {

  }

  calendars = graph_client.get('{0}/me/calendars'.format(graph_url))

  return calendars.json()['value']


def get_calendar_events(token):

  graph_client = OAuth2Session(token=token)

  query_params = {
    '$select': 'subject,organizer,start,end',
    '$orderby': 'createdDateTime DESC'
  }

  events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)

  return events.json()

def create_calendar(token, name="ALA Calendar"):

  calendarId=None

  for l in range(5):

    graph_client = OAuth2Session(token=token)
    query_params = {
          'name':name,
      }
      
    calendar = graph_client.post(
        '{0}/me/calendars'.format(graph_url),
        json=query_params,
        headers=headers
        )
    calendarId = calendar.json().get('id', None)
    
    if calendarId!=None:
      break
    else:
      name+=str(l)

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

def rruleToMSRecurrence(rrule, startDate, endDate):
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
      "endDate": "2020-09-01" #endDate[:10],
    }
    }
  }

  
  return recurrence

def toTwoDigits(a):
  
  if a<10:
    a="0"+str(a)

  return a

def getEndTime(startTime, duration):

    startTimeSplited = startTime.split(':')
    startTimeInHour = int(startTimeSplited[0]) + int(startTimeSplited[1])/60
    EndTime = startTimeInHour + duration

    a = int(EndTime)
    b = int((EndTime - int(EndTime))*60)

    EndTime = '{}:{}'.format(toTwoDigits(a),toTwoDigits(b))
    
    return EndTime

def getOffsetDate(start, offset):

  # Find the exact date
  print("Start", start)
  year, month, day = start.split('-')
  

  date = "{}-{}-{}".format(year, month, toTwoDigits(int(day)+int(offset)))

  return date


def create_events(token, calendarId, courses, start, end):
  
  # Format for start and end: 2020-09-18
  # End format: YYYYMMDD

  end = end.replace('-','')
  
  colors = 'Gray Blue Red Yellow Green Purple'.split()
  locations = 'LC1 LC2 LC5 LC10 MST2 LC4'.split() #**Implement real locations
  
  graph_client = OAuth2Session(token=token)

  for block, subject in enumerate(courses): #self.user.courses:
  # Go over every subjects
      print('block', block, subject)

      for i, eventBlock in enumerate(eventData[block]):
        # Go over the reccurent group of the subject
          
          eventStartDate = getOffsetDate(start, eventBlock['offset'])

          print(i,
          "Start", '{}T{}:00'.format(eventStartDate, eventBlock['start']),
          "End", '{}T{}:00'.format(eventStartDate, getEndTime(eventBlock['start'], eventBlock['duration'])))

          event = {
              'Subject': subject + "-{}-{}".format(block,i),
              'Location':{
                'displayName':locations[block]
                } ,
              "Body": {
                "ContentType": "HTML",
                "Content": "This is the course description"
                },
              'start': {
                  'dateTime': '{}T{}:00'.format(eventStartDate, eventBlock['start']),
                  'timeZone': 'South Africa Standard Time',
              },
              'end': {
              'dateTime': '{}T{}:00'.format(eventStartDate, getEndTime(eventBlock['start'], eventBlock['duration'])),
              'timeZone': 'South Africa Standard Time',
              },
              'categories': ['{} category'.format(colors[block])],
              'recurrence': rruleToMSRecurrence(
                eventBlock['recurrence']+';UNTIL={}T235900Z'.format(end),
                startDate = '{}T{}:00'.format(eventStartDate, eventBlock['start']),
                endDate = '{}T{}:00'.format(end, eventBlock['start'])
                )['recurrence'],
          }
          
          eventResponse = graph_client.post(
            '{0}//me/calendars/{1}/events'.format(graph_url,calendarId),
            json=event,
            headers=headers)
          #if eventResponse.json().get('error')!=None:
          #  print("error", print(eventResponse.json()))

          print(eventResponse.json())
          #help(eventResponse)