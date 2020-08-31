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

def getOffsetDate(start, offset):

  # Find the exact date
  #print("Start", start)
  year, month, day = start.split('-')
  

  date = "{}-{}-{}".format(year, month, toTwoDigits(int(day)+int(offset)))

  return date


def create_events(token, calendarId, courses, startDate, endDate, template):
  
  # Format for start and end: 2020-09-18
  # End format: YYYYMMDD

  # TODO: Set activities/courses to fit the selection list from the UI
  courses = 'A B C D E F G H I J K L M N O P Q R S'.split()

  # TODO: Set colors to fit the number of activities/courses
  colors = 'Gray Blue Red Yellow Green Purple Gray Blue Red Yellow Green Purple'.split()

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

  for week in weeks:
    
    cells = week.cells.all()
    nbrCells = len(cells)

    for l in range(6): 

      pastColor = cells[l]
      pastTime = startTime
      currentTime = startTime
      BYDAY = 'MO TU WE TH FR SA'.split()

      print("Value of l: (0-5)", l)
      for i in range(1, nbrCells//6): # Will be the number of lines in the table
        # i+l is going through the table by column
        
        currentColor = cells[l + i*6]
        print("Value of i : ", i, pastColor.color, currentColor.color, pastColor.id, currentColor.id)
        currentTime += timedelta(minutes=interval)

        if currentColor.color!=pastColor.color: # New block

          pastColor=currentColor
          pastTime=currentTime

          # Save the block, from the pastTime to the currentTime
          # pastBlock: pastTime to currentTime with 

          # TODO: If the last block only last 'interval' time long, there will be an error :)
          # FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2

          # Time format: 'HHTMM:SS
          recurrence = {
            "recurrence": {
              "pattern": {
                "type": 'weekly',
                "interval": str(cycle),
                "daysOfWeek": BYDAY[l],
                },
              "range": {
                "type": "endDate",
                "startDate": startDate,
                "endDate": endDate 
                }
              }
            }
          
          pastSeconds = pastTime.seconds
          pastHours = toTwoDigits(
            pastSeconds // 3600
            )
          pastMinutes = toTwoDigits(
            (pastSeconds % 3600) // 60
            )

          currentSeconds = currentTime.seconds
          currentHours = toTwoDigits(
            currentSeconds // 3600
          )
          currentMinutes = toTwoDigits(
            (currentSeconds % 3600) // 60
          )

          event = {
              'Subject': courses[pastColor.color],
              'Location':{
                'displayName':'virtual'
              } ,
              "Body": {
                  "ContentType": "HTML",
                  "Content": "This is the course description"
              },
              'start': {
                'dateTime': "{}T{}:00".format(pastHours, pastMinutes),
                'timeZone': 'South Africa Standard Time',
              },
              'end': {
                'dateTime': "{}T{}:00".format(currentHours, currentMinutes),
                'timeZone': 'South Africa Standard Time',
                },
              'categories': ['{} category'.format(colors[pastColor.color])],
              #'recurrence': recurrence,
          }
          #print(event)
          #print()
        # End if :)

        # TODO: Test saving the calendar
        #         
        eventResponse = graph_client.post(
        '{0}//me/calendars/{1}/events'.format(graph_url,calendarId),
        json=event,
        headers=headers)
        
        if eventResponse.json().get('error')!= None:
          print("error", print(eventResponse.json()))

      #print(eventResponse.json())
      #help(eventResponse)