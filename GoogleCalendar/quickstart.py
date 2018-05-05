"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.

EXAMPLE FROM GOOGLE 


"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import json

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time 
tmrrw = datetime.datetime.utcnow() + datetime.timedelta(1)  
tomorrow = tmrrw.isoformat() + 'Z'
# print(now)
# print(tomorrow)
# print('Getting the upcoming 10 events')


events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,      
                                      singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    summary = event['summary']
    summary = summary.lower()
    if 'meeting:' in summary:
        if event['attendees']:
            attendees = event['attendees']
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            print(attendees)
    
    
    # attendees = event['attendees']
    # print(json.dumps(event, indent=2))
    # attendees = event['attendees'].get('displayName')
    # print(start, event['summary'])
    # print(attendees)