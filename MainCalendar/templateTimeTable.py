import pandas as pd

DATA_LOCATION = '~/Documents/Projects/TimeManagement/MainCalendar/Template.xlsx'

df = pd.read_excel(DATA_LOCATION, sheet_name='Timetable',
usecols=range(1, 14),
nrows=40,
skiprows=2
)


time = df.iloc[ :,:1]
blockA = df.iloc[:, 1:7]
blockB = df.iloc[:, 8:13]

# Iter over a dataframe
# will need to iter over the 2 dataframe: Find how tomorrow :)
for index, row in time.iterrows():
    
    print(row[0])


# TODO: Match the timeslot to the block, day and week cycle (A or B)
# TODO: Record the data on the user calendar