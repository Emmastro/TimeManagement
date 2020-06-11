
# data[COLOR_ID][RECURENCE_CAT_ID][PROPERTY]

snack = None

lunch = None

dinner = None

start = 0 # Starting date

duration = 0 # Ending date // Format: YYYYMMDD

#start: YYYY-MM-DDThh:mm:ss

def getEndTime(startTime, duration):

    print('startTime', startTime)
    startTimeSplited = startTime.split(':')
    startTimeInHour = int(startTimeSplited[0]) + int(startTimeSplited[1])/60
    print('startTimeInHour', startTimeInHour, duration)
    EndTime = startTimeInHour + duration
    
    
    
    EndTime = '{}:{}'.format(int(EndTime), int((EndTime - int(EndTime))*60))
    
    return EndTime



eventData = [
# Grey Block 0
[
    # Week A 1
    {
        'offset':0,
        'start':'08:00',
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week A 2
    {
        'offset':1,
        'start': '11:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
    # Week A* 3
    {
        'offset':19,
        'start': '09:00', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 4
    {
        'offset':7,
        'start': '13:15', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week B 5
    {
        'offset':9,
        'start': '09:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },

],
# Blue block 1
[
    # Week A 6
    {
        'offset':0,
        'start': '09:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week A 7
    {
        'offset':1,
        'start': '13:15', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU;INTERVAL=2',
    },
    # Week A 8
    {
        'offset':4,
        'start': '13:15', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2',
    },
    # Week A* 9
    {
        'offset':19,
        'start': '10:00', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 10
    {
        'offset':8,
        'start': '08:00', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
    # Week B 11
    {
        'offset':9,
        'start': '11:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
],
# Red Block 2
[  
    # Week A 12
    {
        'offset':0,
        'start': '11:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO;INTERVAL=2',
    },
    # Week A 13
    {
        'offset':2,
        'start': '08:00', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
    # Week A 14
    {
        'offset':3,
        'start': '11:00', 
        'duration':1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=TH;INTERVAL=2',
    },
    # Week A 15
    {
        'offset':4,
        'start': '14:30', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2',
    },
    # Week A* 16
    {
        'offset':19,
        'start': '11:30', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 17
    {
        'offset':8,
        'start': '09:00', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
    # Week B 18
    {
        'offset':9,
        'start': '13:15', 
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
],
# Yellow Block
[
    # Week A 19
    {
        'offset':0,
        'start':'13:15',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week A 20
    {
        'offset':2,
        'start':'09:00',
        'duration': 1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
    # Week A 21
    {
        'offset':5,
        'start':'09:00',
        'duration':1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 22
    {   
        'offset':7,
        'start':'08:00',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week B 23
    {
        'offset':8,
        'start':'11:00',
        'duration': 1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
],
# Green block
[
    # Week A 24

    {
        'offset':1,
        'start':'08:00',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
    # Week A 25
    {
        'offset':2,
        'start':'11:00', 
        'duration': 1.5, 
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
    # Week A 26
    {
        'offset':5,
        'start':'10:00',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 27
    {
        'offset':7,
        'start':'09:00',
        'duration': 1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO,TH;INTERVAL=2',
    },
    # Week B 28
    {
        'offset':8,
        'start':'13:15',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU;INTERVAL=2',
    },
    # Week B 29
    {
        'offset':11,
        'start':'13:30',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2',
    },
],
# Purple Block
[
    # Week A 30
    {
        'offset':1,
        'start':'09:00',
        'duration': 1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=TU,FR;INTERVAL=2',
    },
    # Week A 31
    {
        'offset':2,
        'start':'13:15',
        'duration': 1, 
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
    # Week A 32
    {
        'offset':5,
        'start':'11:30',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=SA;INTERVAL=4',
    },
    # Week B 33
    {
        'offset':7,
        'start':'11:00',
        'duration': 1.5,
        'recurrence':'FREQ=WEEKLY;BYDAY=MO;INTERVAL=2',
    },
    # Week B 34
    {
        'offset':9,
        'start':'08:00',
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=WE;INTERVAL=2',
    },
    # Week B 35
    {
        'offset':10,
        'start':'11:30', 
        'duration': 1,
        'recurrence':'FREQ=WEEKLY;BYDAY=TH;INTERVAL=2',
    },
    # Week B 36
    {
        'offset':11,
        'start':'14:30', 
        'duration': 1, 
        'recurrence':'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2',
    },
]    
]