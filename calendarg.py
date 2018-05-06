import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json


# Setup the Calendar API
def setup(telegram_id):
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    return service


def next_meeeting(timeDeltaInSeconds=61):
    service = setup(telegram_id=1234)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time 
    # next_min = datetime.datetime.utcnow() + datetime.timedelta(,timeDeltaInSeconds) # nextMin is used for timeMax, which is exclusive
    # nextMin = next_min.isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=1,
                                        singleEvents=True,
                                        orderBy='startTime').execute()


    events = events_result.get('items', [])
    
    return events[0]


def main():
    # Call the Calendar API
    # service = setup(telegram_id=1234)
    # next_meeeting(service)

    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time 
    # tmrrw = datetime.datetime.utcnow() + datetime.timedelta(1)  
    # tomorrow = tmrrw.isoformat() + 'Z'

    # events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,      
    #                                     singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     summary = event['summary']
    #     summary = summary.lower()
    #     if 'meeting:' in summary:
    #         if event['attendees']:
    #             attendees = event['attendees']
    #             start = event['start'].get('dateTime', event['start'].get('date'))
    #             end = event['end'].get('dateTime', event['end'].get('date'))

    #             print(attendees, start, end)
    pass
