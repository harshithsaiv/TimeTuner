import openai
import os
from dotenv import load_dotenv
from calendar_manager import authenticate_google_calendar, check_availability, create_event
import datetime
from openai import OpenAI

load_dotenv() 

def parse_office_hours(office_hours_str):
    """Parse office hours from a multi-line string into a dictionary."""
    office_hours = {}
    lines = office_hours_str.strip().split('\n')
    for line in lines:
        clean_line = line.strip().replace('\r', '')
        if ':' in clean_line:
            day_part, times = clean_line.split(': ')
            day = day_part.split()[-1]
            start_time_str, end_time_str = times.split(' to ')
            office_hours[day] = (start_time_str.strip(), end_time_str.strip())
    return office_hours

def is_appointment_valid(day, time_str, office_hours):
    """Check if the proposed appointment time is within the office hours for a given day."""
    if day not in office_hours:
        return False
    start_time_str, end_time_str = office_hours[day]
    start_time = datetime.datetime.strptime(start_time_str, "%I:%M%p").time()
    end_time = datetime.datetime.strptime(end_time_str, "%I:%M%p").time()
    appointment_time = datetime.datetime.strptime(time_str, "%I:%M%p").time()
    return start_time <= appointment_time <= end_time


def get_response(client, message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    return response.choices[0].message.content

def chat_with_chatgpt(office_hours_str):
    """Interact with the user to schedule appointments based on office hours using ChatGPT."""
    service = authenticate_google_calendar()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    office_hours = parse_office_hours(office_hours_str)
    client=OpenAI()
    messages=[]
    
    messages.append({"role":"system","content":"Greet the user and inform that you are a appointment booking assistant. Ask the user to input his name"})
    greeting = get_response(client,messages)
    print(greeting)
    messages.append({"role":"assistant","content":greeting})
    x=input()
    messages.append({"role":"user","content":x})
    print(messages) #debug
    
    # print("Welcome to our appointment scheduling system.")
    print("Here are our office hours:")
    for day, times in office_hours.items():
        print(f"{day}: {times[0]} to {times[1]}")
    # print("Please enter the day and time you'd like to schedule your appointment (e.g., 'Mon 11:00am').")
    
    while True:
        try:
            messages.append({"role":"system","content":"Ask the user to enter the day and time they like to schedule the appointment (e.g., Tue 2:00pm):"})
            # appointment_query = f"{user_name}, please ask the user to enter the day and time they like to schedule the appointment (e.g., Tue 2:00pm):"
            appointment_time = get_response(client,messages)
            messages.append({"role":"assistant","content":appointment_time})
            print(appointment_time)
            user_input = input()  #Input for the day and time
            messages.append({"role":"user","content":user_input})
            day, time_str = user_input.split()
            print("day",day)
            print("time_str",time_str)
            print(messages) #debug
            
            is_free, time_range = check_availability(service, day, time_str, office_hours)
            if is_appointment_valid(day, time_str, office_hours) and is_free:
                messages.append({"role":"system","content":"Generate a polite confirmation message for user an appointment scheduled on the date they mentioned"})
                # confirmation_prompt = f"Generate a polite confirmation message for user with name {user_name} an appointment scheduled on {day} at {time_str}."
                confirmation_message = get_response(client, messages)
                messages.append({"role":"assistant","content":confirmation_message})
                print(time_range)
                start_time, end_time = time_range.split('/')
                print("start_time",start_time)
                print("End_time",end_time)
                title = input("Enter the title of the meeting: ")
                event_link = create_event(service, start_time, end_time, title)
                print(f"{confirmation_message}\nYou can view the event here: {event_link}")
                break
            else:
                messages.append({"role":"system","content":"Sorry, the requested time slot is not available. Please choose a different time."})
                unavailable_time = get_response(client, messages)
                print(unavailable_time)
        except ValueError:
            messages.append({"role":"system","content":"Please enter a valid day followed by time in the format 'Day HH:MMam/pm'. Example: Tue 2:00pm"})
            # error_message = "Please enter a valid day followed by time in the format 'Day HH:MMam/pm'. Example: Tue 2:00pm"
            print(get_response(client, messages))
        except Exception as e:
            error_handling = f"An error occurred: {str(e)}"
            print(get_response(client, error_handling))
            