from django.shortcuts import render
from Accounts.auth_helper import get_token, initialize_context
from .graph_helper import get_calendar_events
import dateutil


#Microsoft Graph secret: nuhzoYUFI0935_*trHHX3#@
#client d7445665-43de-4990-a09a-215ca2e6706a

def calendar(request):
  context = initialize_context(request)

  token = get_token(request)

  events = get_calendar_events(token)

  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'calendar.html', context)

