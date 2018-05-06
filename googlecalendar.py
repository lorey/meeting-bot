import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# Setup the Calendar API
def setup():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('data/credentials/google_calendar.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('data/credentials/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    return service


def next_meeeting(within_seconds=61):
    # call setup if needed
    service = setup()

    now_str = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    next_min = datetime.datetime.utcnow() + datetime.timedelta(seconds=within_seconds + 1)  # nextMin is used for timeMax, which is exclusive
    next_min_str = next_min.isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now_str,
        timeMax=next_min_str,
        singleEvents=True,
        orderBy='startTime').execute()

    next_events = events_result['items']
    return next_events[0]


def main():
    print(next_meeeting(100000))
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


if __name__ == '__main__':
    main()
