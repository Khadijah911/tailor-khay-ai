from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google_calendar.calendar_auth import get_calendar_service
from google_calendar.calendar_utils import make_datetime

from mcp.server import Server
from mcp import types

import anyio
from mcp.server.stdio import stdio_server

LAGOS = ZoneInfo("Africa/Lagos")

def make_datetime(date, time):
    return datetime.strptime(
        f"{date} {time}",
        "%Y-%m-%d %H:%M"
    ).replace(tzinfo=LAGOS)



def check_calendar(date : str,time : str ):
  """
 
Use this tool ONLY when the customer wants to check whether a specific appointment slot is available.

Before calling this tool, make sure BOTH the appointment date and appointment time have been provided.

Do NOT use this tool to make a booking.
"""
 

  service = get_calendar_service()
  start_datetime = make_datetime(date, time)
  end_datetime = start_datetime + timedelta(hours=1)
  
  # Check working days (Monday=0 ... Sunday=6)
  if start_datetime.weekday() == 6:
      return {
          "status": "error",
          "message": "Appointments are available only from Monday to Saturday."
      }

  # Check business hours (9:00 AM - 5:00 PM)
  if not (9 <= start_datetime.hour < 17):
      return {
          "status": "error",
          "message": "Appointments can only be booked between 9:00 AM and 5:00 PM."
      }
  
  if start_datetime < datetime.now(ZoneInfo("Africa/Lagos")):
    return {
        "status": "error",
        "message": "Appointments can only be booked for a future date and time."
    }

  result=service.events().list(
    calendarId="primary",
    timeMin=start_datetime.isoformat(),
    timeMax=end_datetime.isoformat(),
    singleEvents=True,
    orderBy="startTime"
    ).execute()

  events=result.get('items',[])
  if not events:
    return{"status": "available"}
        
  return {"status": "booked"}


def book_appointment(date : str,time : str,customer_name : str ,phone_number : str,purpose : str):
  """
  Use this tool ONLY when the customer wants to book an appointment.

  This tool reserves the appointment date and stores the customer's
  name, phone number, preferred time, and appointment purpose.
  """

  service = get_calendar_service()
  start_datetime = make_datetime(date, time)
  end_datetime = start_datetime + timedelta(hours=1)


  if start_datetime.weekday() == 6:
      return {
          "status": "error",
          "message": "Appointments are available only from Monday to Saturday."
      }


  if not (9 <= start_datetime.hour < 17):
      return {
          "status": "error",
          "message": "Appointments can only be booked between 9:00 AM and 5:00 PM."
      }

  if start_datetime < datetime.now(ZoneInfo("Africa/Lagos")):
    return {
        "status": "error",
        "message": "Appointments can only be booked for a future date and time."
    }
  result=service.events().list(
    calendarId="primary",
    timeMin=start_datetime.isoformat(),
    timeMax=end_datetime.isoformat(),
    singleEvents=True,
    orderBy="startTime"
    ).execute()

  events=result.get('items',[])
  if events:
    return{
      'status':'error',
      'message':'The selected date and time are already booked. Please choose another time'
    }

  event ={
      'summary':purpose,
    "description": f"Appointment for {customer_name}",
  "extendedProperties": {
        "private": {
            "customer_name": customer_name,
            "phone_number": phone_number,
            'purpose' : purpose
        }
    },
  'start' :{
  'dateTime':start_datetime.isoformat(),
  'timeZone':'Africa/Lagos'},
  
  'end':{
  'dateTime': end_datetime.isoformat(),
  'timeZone':'Africa/Lagos'}
  }

  created_event= service.events().insert(
      calendarId='primary',
      body=event  
  ).execute()

  return{'status' : 'success',
             'customer_name': customer_name,
             'message' : f"Your appointment for {purpose} has been booked successfully for {date}."}
  



def cancel_appointment(phone_number: str,customer_name: str):
  """
Cancel an appointment booked by the customer and make the date available for booking
Use this tool ONLY when the customer wants to cancel an existing appointment.

The tool searches for the customer's appointment and removes it from the calendar.
"""

  print("cancel_appointment tool called")

  
  service = get_calendar_service()

  result=service.events().list(
  calendarId="primary",
  singleEvents=True,
    ).execute()
  events=result.get('items',[])

  for event in events:

    private = event.get(
        "extendedProperties",
        {}
    ).get(
        "private",
        {}
    )

    if private.get("phone_number") == phone_number:
        service.events().delete(calendarId="primary",
         eventId=event["id"] ).execute()

        return {
        "status": "success",
        "message": "Your appointment has been cancelled successfully."
        }
  return {
    "status": "error",
    "message": "I couldn't find any appointment with that phone number."
    }



def view_appointments(date : str):

  """
View all appointments scheduled for a given date.
Returns the customer's appointment details if the date is booked.
"""

  service = get_calendar_service()

  start_datetime= datetime.strptime(date, '%Y-%m-%d')
  end_datetime= start_datetime + timedelta(days=1)

  result=service.events().list(
  calendarId="primary",
  timeMin=start_datetime.isoformat() + "Z",
  timeMax=end_datetime.isoformat() + "Z",
  singleEvents=True,
  orderBy="startTime"
    ).execute()

  events=result.get('items',[])
  if not events:
      return{
        'status' : 'success',
        'message' : f'No appointments for {date}'
    }

  appointments=[]
  for event in events:
    appointments.append({
           "customer_name": event.get("description", "No description"),
        "purpose": event.get("summary", "No purpose"),
        "start_time": event["start"].get("dateTime"),
        "end_time": event["end"].get("dateTime"),
          }
          )
  return {
          'status' : 'success',
          'appointments': appointments
      }

def reschedule_appointment(
    phone_number: str,
    new_date: str,
    new_time: str,
    customer_name: str
):
    """move an appointment from an old date to a new date
the customer's details, appointment time, and purpose.
"""

    service = get_calendar_service()

    if start_datetime.weekday() == 6:
        return {
            "status": "error",
            "message": "Appointments are available only from Monday to Saturday."
        }

    if not (9 <= start_datetime.hour < 17):
        return {
            "status": "error",
            "message": "Appointments can only be booked between 9:00 AM and 5:00 PM."
        }
    
    if start_datetime < datetime.now(ZoneInfo("Africa/Lagos")):
        return {
            "status": "error",
            "message": "Appointments can only be booked for a future date and time."
        }

    result = service.events().list(
        calendarId="primary",
        singleEvents=True,
    ).execute()

    events = result.get("items", [])

    
    appointment = None

    for event in events:
        private = event.get(
            "extendedProperties",
            {}
        ).get(
            "private",
            {}
        )

        if private.get("phone_number") == phone_number:
            appointment = event
            break

 
    if appointment is None:
        return {
            "status": "error",
            "message": "Appointment not found."
        }

    
    new_start = datetime.strptime(
        f"{new_date} {new_time}",
        "%Y-%m-%d %H:%M"
    ).replace(tzinfo=ZoneInfo("Africa/Lagos"))

    new_end = new_start + timedelta(hours=1)

    
    result = service.events().list(
        calendarId="primary",
        timeMin=new_start.isoformat(),
        timeMax=new_end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events_in_slot = result.get("items", [])

    for event in events_in_slot:
        if event["id"] != appointment["id"]:
            return {
                "status": "error",
                "message": "The new date and time is already booked."
            }
    appointment["start"] = {
    "dateTime": new_start.isoformat(),
    "timeZone": "Africa/Lagos"
  }

    appointment["end"] = {
      "dateTime": new_end.isoformat(),
      "timeZone": "Africa/Lagos"
  }  

    updated_event = service.events().update(
      calendarId="primary",
      eventId=appointment["id"],
      body=appointment
  ).execute()

    return {
      "status": "success",
      "customer_name": customer_name,
      "message": (
          f"Your appointment has been rescheduled to "
          f"{new_date} at {new_time}."
      )
  }


def update_appointment(customer_name : str, phone_number : str,new_customer_name : str="",new_phone_number : str="", new_purpose : str=""):


  """ help update client appointment details with the new information provided"""
  service = get_calendar_service()
  result=service.events().list(
  calendarId="primary",
  singleEvents=True ).execute()
  events=result.get('items',[])

  for event in events:

    private = event.get(
        "extendedProperties",
        {}
    ).get(
        "private",
        {}
    )
    if ( private.get("phone_number") == phone_number and private.get("customer_name") == customer_name):
      updated = False
      if new_phone_number:
        private["phone_number"]= new_phone_number
        updated = True
      if new_customer_name:
        private['customer_name'] = new_customer_name
        event['description'] = f"Appointment for {new_customer_name}"
        updated = True
      if new_purpose:
        private['purpose'] = new_purpose
        event["summary"] = new_purpose
        updated = True
      if not updated:
        return {
            "status": "error",
            "message": "No new information was provided to update."
        }
      service.events().update(calendarId="primary",
         eventId=event["id"],body=event ).execute()

      return {
    "status": "success",
    "customer_name": private["customer_name"],
    "message": "Your appointment details have been updated successfully."
}
  return {
    "status": "error",
    "message": "I couldn't find any appointment with the provided name and phone number."
    }

def show_all_appointments():
    """
    Return all booked appointments and their details for Tailor Khay.
    """

    service = get_calendar_service()

    result = service.events().list(
        calendarId="primary",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = result.get("items", [])

    if not events:
        return {
            "status": "error",
            "message": "There are no booked appointments."
        }

    appointments = []

    for event in events:

        private = event.get(
            "extendedProperties",
            {}
        ).get(
            "private",
            {}
        )

        appointments.append({
            "customer_name": private.get("customer_name"),
            "phone_number": private.get("phone_number"),
            "purpose": event.get("summary"),
            "start_time": event["start"].get("dateTime"),
            "end_time": event["end"].get("dateTime")
        })

    return {
        "status": "success",
        "appointments": appointments
    }

def show_available_time_slots(date:str):
  """
Use this tool when a customer asks:
 What times are available on a particular date?
Show available appointment slots.
What appointment times are free?
Which times can I book on a given date?
The tool returns every available one-hour appointment slot between
9:00 AM and 5:00 PM for the requested date.
"""
  service=get_calendar_service()

  start_datetime = datetime.strptime(
    f"{date}",
    "%Y-%m-%d"
).replace(tzinfo=ZoneInfo("Africa/Lagos")
)
  end_datetime = start_datetime + timedelta(days=1)

  result=service.events().list(
    calendarId="primary",
    timeMin=start_datetime.isoformat(),
    timeMax=end_datetime.isoformat() ,
    singleEvents=True,
    orderBy="startTime"
    ).execute()

  events=result.get('items',[])

  business_slots=[]
  for i in range (9,17):
      slot_start = datetime.strptime(
        f"{date} {i}:00",
        "%Y-%m-%d %H:%M"
      ).replace(tzinfo=ZoneInfo("Africa/Lagos"))

      booked=False

      for event in events:

        event_start=event['start']['dateTime']

        event_start=datetime.fromisoformat(event_start)
        if event_start == slot_start:
          booked=True
          break

      if not booked:
          business_slots.append(slot_start.strftime("%I:%M %p"))
  if business_slots:
    return{ "status" : "success",
    "date" : date,
    "available_slots": business_slots
    }
  return{ "status": "full",
        "message": "There are no available appointment slots for this date."
        }
