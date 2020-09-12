from requests_oauthlib import OAuth2Session
from MainCalendar.models import TimeTableTemplate
from datetime import datetime  
from datetime import timedelta  

graph_url = 'https://graph.microsoft.com/v1.0'
headers = {"Content-Type": "application/json"}

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Dimanche']

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
    for fullday in DAYS:
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


class EventData:

  def __init__(self, blocks, startDate, endDate):
    
    self.blocks = blocks
    self.startDate = startDate
    self.endDate = endDate

  def setEvent(self, pastColor, day, nweek, pastHours, pastMinutes, currentHours, currentMinutes, cycle, dayOfWeek):


    colors = "Blue Red Yellow Green Grey Purple Black Orange Orange Orange Orange Orange Orange Orange".split()
    
    return {
      'Subject': self.blocks[pastColor.color-1],
      'Location':{
        'displayName':'virtual'
      } ,
      "Body": {
          "ContentType": "HTML",
          "Content": "This is the course description"
      },
      'start': {
        'dateTime': "{}T{}:{}:00".format(getOffsetDate(self.startDate, day, nweek) , pastHours, pastMinutes),
        'timeZone': 'South Africa Standard Time',
      },
      'end': {
        'dateTime': "{}T{}:{}:00".format(getOffsetDate(self.startDate, day, nweek), currentHours, currentMinutes),
        'timeZone': 'South Africa Standard Time',
        },
      'categories': ['{} category'.format(colors[pastColor.color-1])],
      'recurrence': {
        "pattern": {
          "type": 'weekly',
          "interval": str(cycle),
          "daysOfWeek": [dayOfWeek] ,
          },
        "range": {
          "type": "endDate",
          "startDate": getOffsetDate(self.startDate, day, nweek),
          "endDate": self.endDate 
          }
        },
    }


def create_events(token, calendarId, blocks, startDate, endDate, template):
  
  requests = {
    'requests' : [],
  }
  requestID = 1
  allRequests = []
  # TODO: Set real locations
  locations = ['LC1', 'LC2', 'LC5', 'LC10', 'MST2', 'LC4']
  
  graph_client = OAuth2Session(token=token)

  timeTableTemplate = TimeTableTemplate.objects.get(id=template)
  weeks = timeTableTemplate.weeks.all()
  cycle = len(weeks)

  interval = timeTableTemplate.interval
  startTime = timeTableTemplate.start
  startTime = timedelta(hours=startTime.hour, minutes=startTime.minute)

  endTime = timeTableTemplate.end
  endTime = timedelta(hours=endTime.hour, minutes=endTime.minute)

  eventData = EventData(blocks, startDate, endDate)
  
  for nweek, week in enumerate(weeks):
    
    cells = week.cells.all()
    nbrCells = len(cells)

    # Go over each column in the timetable, representing days
    for day in range(6): 

      pastColor = cells[day]
      pastTime = startTime
      currentTime = startTime
      BYDAY = DAYS

      # Go over each line in the timetable, representing timeslots 
      for slot in range(nbrCells//6 ):  
        last=False
        
        try: # If it's not the last block
          currentColor = cells[day + (1+slot) *6]
        except: # If it's the last block
          last=True

        currentTime += timedelta(minutes=interval)

        # The timeslot color has changed, meaning it's a new time block
        if currentColor.color!=pastColor.color or last==True:

           # Color 0 is a free block
          if pastColor.color!=0:
            
          
            pastHours = toTwoDigits(pastTime.seconds // 3600)
            pastMinutes = toTwoDigits((pastTime.seconds % 3600) // 60)

            currentHours = toTwoDigits(currentTime.seconds // 3600)
            currentMinutes = toTwoDigits((currentTime.seconds % 3600) // 60)
          
            event = eventData.setEvent(pastColor, day, nweek, pastHours, pastMinutes, currentHours, currentMinutes,
            cycle, BYDAY[day])
            
            requests['requests'].append(
              {
                "id": str(requestID),
                "url": '/me/calendars/{}/events'.format(calendarId),
                "method": "POST",
                "body": event.copy(),
                "headers": {
                  "Content-Type": "application/json"
                  #"Accept": "application/json"
                }
              }
            )
            
            requestID+=1
            if requestID == 5:
              allRequests.append(requests.copy())
              requests['requests'] = []
              requestID=1


          pastColor = currentColor
          pastTime = currentTime
  print(allRequests)

  for r in allRequests:
    print("R", r)
    eventResponse = graph_client.post(
      'https://graph.microsoft.com/v1.0/$batch',
      json=r,
      headers=headers)

    print("RESPONSE: ", eventResponse)
    
  if eventResponse.json().get('error')!= None:

    print("error", print(eventResponse.json()))