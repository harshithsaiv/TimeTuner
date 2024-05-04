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
        print(f"Day '{day}' is not a valid office day.")
        return False, None

    # Define timezone
    timezone = 'America/Los_Angeles'

    # Get the current datetime in the specified timezone.
    current_datetime = datetime.datetime.now(pytz.timezone(timezone))
    current_date = current_datetime.date()
    current_weekday_str = current_datetime.strftime('%a')  # e.g., "Mon"

    # Find index for current and target days of the week
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    current_weekday_index = days_of_week.index(current_weekday_str)  # Current weekday index
    target_weekday_index = days_of_week.index(day)  # Target weekday index

    # Calculate how many days to add to current date to reach the next occurrence of 'day'
    days_ahead = (target_weekday_index - current_weekday_index) % 7
    if days_ahead == 0 and current_datetime.strftime('%I:%M%p') >= time_str:
        # If today is the target day but the time has already passed, schedule for next week
        days_ahead += 7

    next_target_date = current_date + datetime.timedelta(days=days_ahead)

    # Convert the appointment time into datetime object
    appointment_start = datetime.datetime.strptime(f'{next_target_date} {time_str}', '%Y-%m-%d %I:%M%p')
    appointment_start = pytz.timezone(timezone).localize(appointment_start)  # Localize to specified timezone
    appointment_end = appointment_start + datetime.timedelta(minutes=30)  # Assuming a 30-minute slot

    # Debug print to check the calculated times
    print(f"Debug: Checking availability from {appointment_start.isoformat()} to {appointment_end.isoformat()}")

    # Ensure the appointment time is within office hours
    office_start_time_str, office_end_time_str = office_hours[day]
    office_start = datetime.datetime.strptime(f'{next_target_date} {office_start_time_str}', '%Y-%m-%d %I:%M%p')
    office_end = datetime.datetime.strptime(f'{next_target_date} {office_end_time_str}', '%Y-%m-%d %I:%M%p')
    office_start = pytz.timezone(timezone).localize(office_start)
    office_end = pytz.timezone(timezone).localize(office_end)

    if not (office_start <= appointment_start < office_end):
        print("The specified time is not within office hours.")
        return False, None

    # Query the calendar for events in the specified time range
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=appointment_start.isoformat(),
            timeMax=appointment_end.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        is_free = len(events) == 0
        return is_free, f'{appointment_start.isoformat()}/{appointment_end.isoformat()}'
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
