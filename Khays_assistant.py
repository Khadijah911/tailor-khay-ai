from inspect import EndOfBlock
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import AIMessage,HumanMessage
from IPython.display import Image, display
from langgraph.graph import START
from langgraph.graph import END
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_core.prompts import MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode,tools_condition
import os
import json

api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key
)


class GraphState(TypedDict):
  ai_message : str
  human_message : str
  intent : str
  should_continue : str
  next_action : str
  messages : Annotated[list,add_messages]

memory=MemorySaver()



def save_calendar():
  with open('calendar.json','w') as file:
    json.dump(calendar,file,indent=4)


def load_calendar():
  with open('calendar.json','r') as file:
    return json.load(file)

calendar =load_calendar()



def collect_customer_message(state):
  print(">>> collect_customer_message")
  user_inquiry =  input('enter you inquiry :')
  return {
      "human_message": user_inquiry,

      'messages' : [HumanMessage(content = user_inquiry)]

  }

from langchain_core.tools import tool


@tool
def check_calendar(date : str):
  """
  Use this tool ONLY when the customer wants to know whether a date is available.
  Do NOT use this tool to make a booking.
  """
  if date in calendar:
    return { 'status' : calendar[date]}
  else:
    return{'status' : 'not available'}


@tool
def book_appointment(date : str,time : str,customer_name : str ,phone_number : str,purpose : str):
  """
  Use this tool ONLY when the customer wants to book an appointment.

  This tool reserves the appointment date and stores the customer's
  name, phone number, preferred time, and appointment purpose.
  """
  if date in calendar:
    if calendar[date]['status'] == 'available':
      calendar[date]['status'] = "booked"
      calendar[date]['customer_name'] = customer_name
      calendar[date]['phone_number'] = phone_number
      calendar[date]['time'] = time
      calendar[date]['purpose'] = purpose

      save_calendar()

      return{'status' : 'success',
             'customer_name': customer_name,
             'time': time,
             'message' : f"Your appointment for {'purpose'} has been booked successfully for {date}."}

    else:
      return {'status' : 'error',
              'message' : 'please pick another date,the date you picked is not available'}

  return{'status': 'error',
       'message' : 'date not found'}



@tool
def cancel_appointment(customer_name: str,date: str):
  """cancel an appointment booked by the customer and make the date available for booking"""

  print("cancel_appointment tool called")


  if date in calendar:
    if calendar[date]['customer_name'].lower() == customer_name.lower() and calendar[date]['status']=='booked':
      calendar[date]['status'] = "available"
      calendar[date]['customer_name'] = None
      calendar[date]['phone_number'] = None
      calendar[date]['time'] = None
      calendar[date]['purpose'] = None

      save_calendar()

      return{
          'status' : 'cancelled',
          'message' : f'The booking for {date} has been sucessfully cancelled'
      }

    else:
      return{'status' : 'error',
             'message' : 'You do not have a booking '}
  else:
    return{
      'status': 'error',
      'message' : 'invalid date,please put in correct date'
    }



@tool
def view_appointments(date : str):
  """
View all appointments scheduled for a given date.
Returns the customer's appointment details if the date is booked.
"""
  if date in calendar:
    if calendar[date]['status'] == 'booked':
      return {
          'status' : 'success',
          'messages': calendar[date]
      }
      save_calendar()
    return{
        'status' : 'success',
        'messages' : f'No appointments for {date}'
    }
  return{
      "status" : 'error',
      'message' : 'invalid date'
  }

@tool
def reschedule_appointment(old_date: str,new_date : str,customer_name: str):
  """move an appointment from an old date to a new date
the customer's details, appointment time, and purpose.
"""
  if old_date in calendar and new_date in calendar:
    if calendar[old_date]['status'] != 'booked':
      return  {'status': 'error',
             'message' : 'There is no appointment for this date.'}

    if calendar[old_date]['customer_name'].lower() != customer_name.lower():
      return  {'status': 'error',
             'message' : 'The appointment does not belong to this customer.'}

    if calendar[new_date]['status'] != 'available':
      return{'status': 'error',
             'message' : 'The new date is already booked.'

      }
    appointment=calendar[old_date].copy()
    calendar[old_date]['status'] = "available"
    calendar[old_date]['customer_name'] = None
    calendar[old_date]['phone_number'] = None
    calendar[old_date]['time'] = None
    calendar[old_date]['purpose'] = None
    calendar[new_date]['status'] = "booked"
    calendar[new_date]['customer_name'] = appointment['customer_name']
    calendar[new_date]['phone_number'] = appointment['phone_number']
    calendar[new_date]['time'] = appointment['time']
    calendar[new_date]['purpose'] = appointment['purpose']

    save_calendar()

    return{'status': 'success',
              'message' : f' {new_date} has been sucessfully booked,rescheduling is sucessful'}


  return{ "status" : 'error',
      'message' : 'invalid date'

  }
  


model_with_tools = model.bind_tools([check_calendar,book_appointment,cancel_appointment,reschedule_appointment,view_appointments,
])
tool_node=ToolNode([check_calendar,book_appointment,cancel_appointment,reschedule_appointment,view_appointments])

def khay_assistant(state):
  print(">>> khay_assistant")

  prompt = ChatPromptTemplate.from_messages([
      ('system' , '''You are Tailor Khay's AI assistant.

You represent Tailor Khay and speak on her behalf. Customers should feel like they are talking directly to Tailor Khay's business.

Your responsibilities include:
Greeting customers warmly and professionally.
Answering questions about appointments and Tailor Khay's services.
Checking appointment availability.
Booking appointments.
Cancelling appointments.
Collecting any information needed to complete a booking.
Handling the entire conversation whenever possible.
If the customer wants to book an appointment, collect all the required information before calling the booking tool.
Only use the view_appointments tool when responding to Tailor Khay, not to customers.

The required information is:
- appointment date
- preferred time
- customer name
- phone number
- appointment purpose

If any of this information is missing, ask the customer for it. Do not make assumptions or guess missing information.

Guidelines:
Be friendly, professional, and polite.
Never make up information. If you do not know something, say so.
Never reveal another customer's personal information, including their name, phone number, appointment time, or booking details.
If information is missing, politely ask only for the missing information.
Do not guess dates, names, phone numbers, or appointment times.
Use the available tools whenever they are needed.
After a tool completes successfully, explain the result naturally to the customer.
If a tool returns an error, politely explain the problem and guide the customer on what to do next.

Pricing:
Do not calculate or estimate prices.
If the customer asks for a price, a quotation, or the cost of a dress or tailoring service, explain that Tailor Khay will personally review the request and provide the final price.
Collect any necessary details about the customer's request before handing the conversation over.
Once all necessary details have been collected, inform the customer that their request has been forwarded to Tailor Khay for pricing.

Your goal is to complete as much of the conversation as possible before involving Tailor Khay.
      '''),

     MessagesPlaceholder('messages')
      ]
    )

  message=prompt.invoke(
     {'messages' : state['messages']}
     )

  response =model_with_tools.invoke(message)
  print(response.content)
  return {
      'ai_message' : response.content,
      'messages' : [ response]

  }

def intent_router(state):

    for i in state['human_message'].lower().split(' '):
      if i in ['much', 'price' , 'cost'] :
        return {
          'intent': 'pricing'
    }

    else:
      return {
          'intent' : 'general'
      }


def pricing (state):
  message='we will handover to tailor_khay to come give you the price'
  print(message)

  return{
      'ai_message' : message,
      'messages' : [AIMessage(content = message)]
  }

graph=StateGraph(GraphState)
graph.add_node('khay_assistant', khay_assistant)


graph.add_node('pricing',pricing)
graph.add_node('intent_router',intent_router)
graph.add_node('tools',tool_node)
graph.add_edge(START , 'intent_router')
graph.add_conditional_edges ('intent_router',
                lambda state : state['intent'],
                {'pricing' : 'pricing',

                'general' : 'khay_assistant'
                 })
graph.add_conditional_edges( 'khay_assistant', tools_condition)
graph.add_edge('tools','khay_assistant')
graph.add_edge('khay_assistant',END)
graph.add_edge('pricing' , END)

app=graph.compile(checkpointer=memory)

while True:

  user_inquiry = input('Enter your inquiry: ')

  if user_inquiry.lower() == 'bye':
    print('goodbye')

    break

  app.invoke({ 'human_message' : user_inquiry,
  'messages' : [HumanMessage(content=user_inquiry)]
  },
            config = {
                'configurable' : {
                    'thread_id' : 'customer_001'
                }
            })



