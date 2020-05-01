from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scopes)
credentials = flow.run_console()

import pickle

pickle.dump(credentials, open("token.pkl", "wb"))
#In [4]:
credentials = pickle.load(open("token.pkl", "rb"))
#In [5]:
service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()
#In [7]:
print(result['items'][0])
