from icalendar import*

from datetime import*

StartAcademicYear = datetime(2020,9,1,8,0,0)
EndOfAcademicYear = datetime(2021,6,18,8,0,0)

calendar = Calendar()

event = Event()
event['uid'] = '42'
event.add('dtstart', StartAcademicYear)
event.add('dtend', StartAcademicYear + timedelta(hours=1))
event.add('summary', "This is the summary")
event.add('description', "This is the description ...")
event.add('location', "This is the location")
event.add('rrule', {"FREQ": 'weekly', 'interval':2, "UNTIL": EndOfAcademicYear})
event.add('color', 'turquoise')

event1 = Event()
event1['uid'] = '43'
event1.add('dtstart', StartAcademicYear + timedelta(days=2))
event1.add('dtend', StartAcademicYear +  + timedelta(days=2) + timedelta(hours=1))
event1.add('summary', "This is the second summary")
event1.add('description', "This is the second description ...")
event1.add('location', "location 2")
event1.add('rrule', {"FREQ": 'weekly', 'interval':2, "UNTIL": EndOfAcademicYear})
event1.add('color', 'blue')

calendar.add_component(event)
calendar.add_component(event1)


print(calendar)

with open('my.ics', 'wb') as my_file:

    my_file.write(calendar.to_ical())