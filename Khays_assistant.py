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

calendar = {
    "2026-07-10": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-12": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-14": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-16": 
    {
    "status": "booked",
    "customer_name": 'khadijah',
    "phone_number": '09163456069',
    "time": "10:30 AM",
},
    "2026-07-18": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-20": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-22": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-24": 
    {
    "status": "booked",
    "customer_name": 'mary',
    "phone_number": '08023882233',
    "time": "11:20 AM",
},
    "2026-07-26": 
    {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
    "2026-07-30": {
    "status": "available",
    "customer_name": None,
    "phone_number": None,
    "time": None,
},
}

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
def book_appointment(date : str,time : str,customer_name : str ,phone_number : str):
  """
  Use this tool ONLY when the customer wants to book an appointment.
  This tool reserves the date and stores the customer's name, phone number, and preferred time.
  """
  if date in calendar:
    if calendar[date]['status'] == 'available':
      calendar[date]['status'] = "booked"
      calendar[date]['customer_name'] = customer_name
      calendar[date]['phone_number'] = phone_number
      calendar[date]['time'] = time

      return{'status' : 'success',
             'customer_name': customer_name,
             'time': time,
             'message' : f"Your appointment has been booked successfully for {date}."}

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

model_with_tools = model.bind_tools([check_calendar,book_appointment,cancel_appointment])
tool_node=ToolNode([check_calendar,book_appointment,cancel_appointment])


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

def should_continue(state):
  if 'bye' in state['human_message'].lower().split(' '):

      return {
          'next_action': 'stop'
      }


  return{
        'next_action' : 'continue'
      }



graph=StateGraph(GraphState)
graph.add_node('khay_assistant', khay_assistant)
graph.add_node('collect_customer_message', collect_customer_message)

graph.add_node('pricing',pricing)
graph.add_node('intent_router',intent_router)
graph.add_node('continue_router', should_continue)
graph.add_node('tools',tool_node)
graph.add_edge(START,'collect_customer_message')
graph.add_edge('collect_customer_message' , 'intent_router')
graph.add_conditional_edges ('intent_router',
                lambda state : state['intent'],
                {'pricing' : 'pricing',

                'general' : 'khay_assistant'
                 })
graph.add_conditional_edges( 'khay_assistant', tools_condition)
graph.add_edge('tools','khay_assistant')
graph.add_edge('khay_assistant','continue_router')
graph.add_conditional_edges('continue_router',
                            lambda state : state['next_action'],
                            {'continue' : 'collect_customer_message',
                             'stop' : END}
                            )



graph.add_edge('pricing', 'continue_router')

app=graph.compile(checkpointer=memory)
app.invoke({ },
           config = {
               'configurable' : {
                   'thread_id' : 'customer_001'
               }
           })

