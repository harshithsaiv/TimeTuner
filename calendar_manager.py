# calendar_utils.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import pytz

# Define the scope needed for the calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'

def authenticate_google_calendar():
    """Authenticate and return a Google Calendar service object."""
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)
    return service

# def check_availability(service, day, time_str, office_hours):
#     """Check if the time slot is free in the user's Google Calendar."""
#     if day not in office_hours:
#         return False, None
#     start_time_str, end_time_str = office_hours[day]
#     date_today = datetime.datetime.today().date()
#     weekday_today = date_today.strftime('%a')
#     days_ahead = (list(office_hours.keys()).index(day) - list(office_hours.keys()).index(weekday_today)) % 7
#     date_of_appointment = (date_today + datetime.timedelta(days=days_ahead)).isoformat()

#     appointment_start = datetime.datetime.strptime(f'{date_of_appointment} {time_str}', '%Y-%m-%d %I:%M%p')
#     appointment_end = (appointment_start + datetime.timedelta(minutes=30)).isoformat()
#     appointment_start = appointment_start.isoformat()

#     events_result = service.events().list(calendarId=CALENDAR_ID,
#                                           timeMin=appointment_start,
#                                           timeMax=appointment_end,
#                                           singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     return len(events) == 0, f'{appointment_start}/{appointment_end}'


def check_availability(service, day, time_str, office_hours):
    if day not in office_hours:
        return False, None
    start_time_str, end_time_str = office_hours[day]
    date_today = datetime.datetime.now(pytz.timezone('America/Los_Angeles')).date()
    weekday_today = date_today.strftime('%a')
    days_ahead = (list(office_hours.keys()).index(day) - list(office_hours.keys()).index(weekday_today)) % 7
    date_of_appointment = (date_today + datetime.timedelta(days=days_ahead))

    appointment_start = datetime.datetime.strptime(f'{date_of_appointment} {time_str}', '%Y-%m-%d %I:%M%p')
    appointment_start = pytz.timezone('America/Los_Angeles').localize(appointment_start)  # Localize to Los Angeles timezone
    appointment_end = appointment_start + datetime.timedelta(minutes=30)

    print(f"Debug: Checking availability from {appointment_start.isoformat()} to {appointment_end.isoformat()}")  # Debug statement

    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=appointment_start.isoformat(),
            timeMax=appointment_end.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return len(events) == 0, f'{appointment_start.isoformat()}/{appointment_end.isoformat()}'
    except Exception as e:
        print(f"An error occurred while checking availability: {str(e)}")
        return False, None



def create_event(service, start_time, end_time, summary, description=''):
    """Create a calendar event."""
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f'Event created: {event.get("htmlLink")}'
