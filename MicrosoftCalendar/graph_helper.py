from requests_oauthlib import OAuth2Session
from MainCalendar.eventsData import eventData
from MainCalendar.models import TimeTableTemplate
from datetime import datetime  
from datetime import timedelta  

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

def getOffsetDate(start, offset, week):

  year, month, day = map(int, start.split('-'))
  day = day + offset + week * 7 

  if month in [1,3,5,7,8,10,12]:
    #31 days in these months
    if day>31:
      month+=1
      day = day-31
  elif month==2:
    # A whole mess for Fed :)
    #TODO: Consider 28 and 29 days of Feb
    if day>29:
      month+=1
      day = day-31
  else:
    if month>30:
      month+=1
      day = day-31

  if month>12:
    month=1
    year+=1

  date = "{}-{}-{}".format(year, toTwoDigits(month), toTwoDigits(day))

  return date


def setRecurrence(cycle, dayOfWeek, startDate, endDate):

  return {
    "recurrence": {
      "pattern": {
        "type": 'weekly',
        "interval": str(cycle),
        "daysOfWeek": dayOfWeek ,
        },
      "range": {
        "type": "endDate",
        "startDate": startDate,
        "endDate": endDate 
        }
      }
    }

def setEventData(courses, pastColor, startDate, day, nweek, pastHours, pastMinutes, currentHours, currentMinutes):

  colors = 'Gray Blue Red Yellow Green Purple Gray Blue Red Yellow Green Purple Green Yellow Red'.split()

  return {
    'Subject': courses[pastColor.color],
    'Location':{
      'displayName':'virtual'
    } ,
    "Body": {
        "ContentType": "HTML",
        "Content": "This is the course description"
    },
    'start': {
      'dateTime': "{}T{}:{}:00".format(getOffsetDate(startDate, day, nweek) , pastHours, pastMinutes),
      'timeZone': 'South Africa Standard Time',
    },
    'end': {
      'dateTime': "{}T{}:{}:00".format(getOffsetDate(startDate, day, nweek), currentHours, currentMinutes),
      'timeZone': 'South Africa Standard Time',
      },
    'categories': ['{} category'.format(colors[pastColor.color])],
    #'recurrence': recurrence,
          }


def create_events(token, calendarId, courses, startDate, endDate, template):
  
  # Format for start and end: 2020-09-18
  # End format: YYYYMMDD

  # TODO: Set activities/courses to fit the selection list from the UI
  courses = 'A B C D E F G H I J K L M N O P Q R S'.split()

  # TODO: Set colors to fit the number of activities/courses
  
  # TODO: Set real locations
  locations = 'LC1 LC2 LC5 LC10 MST2 LC4'.split() #**Implement real locations
  
  graph_client = OAuth2Session(token=token)

  timeTableTemplate = TimeTableTemplate.objects.get(id=template)
  weeks = timeTableTemplate.weeks.all()
  cycle = len(weeks)

  interval = timeTableTemplate.interval
  startTime = timeTableTemplate.start
  startTime = timedelta(hours=startTime.hour, minutes=startTime.minute)

  endTime = timeTableTemplate.end
  endTime = timedelta(hours=endTime.hour, minutes=endTime.minute)

  
  for nweek, week in enumerate(weeks):
    
    cells = week.cells.all()
    nbrCells = len(cells)

    # Go over each column in the timetable, representing days
    for day in range(6): 

      pastColor = cells[day]
      pastTime = startTime
      currentTime = startTime
      BYDAY = 'MO TU WE TH FR SA'.split()

      # Go over each line in the timetable, representing timeslots 
      for slot in range(nbrCells//6 ):
        print("Slot {}".format(slot))    
        last=False
        # TODO: The current slot should start from the 2nd
        try: # If it's not the last block
          currentColor = cells[day + (1+slot) *6]
        except: # If it's the last block
          last=True

        currentTime += timedelta(minutes=interval)

        # The timeslot color has changed, meaning it's a new time block
        if currentColor.color!=pastColor.color or last==True:

          recurrence = setRecurrence(cycle, BYDAY[day], startDate, endDate)
        
          pastHours = toTwoDigits(pastTime.seconds // 3600)
          pastMinutes = toTwoDigits((pastTime.seconds % 3600) // 60)

          currentHours = toTwoDigits(currentTime.seconds // 3600)
          currentMinutes = toTwoDigits((currentTime.seconds % 3600) // 60)

          event = setEventData(courses, pastColor, startDate, day, nweek, pastHours, pastMinutes, currentHours, currentMinutes)
          
          eventResponse = graph_client.post(
            '{0}//me/calendars/{1}/events'.format(graph_url,calendarId),
            json=event,
            headers=headers)

          pastColor = currentColor
          pastTime = currentTime

          if eventResponse.json().get('error')!= None:
            print("error", print(eventResponse.json()))