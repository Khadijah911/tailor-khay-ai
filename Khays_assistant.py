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
    "2026-07-10": "available",
    "2026-07-12": "available",
    "2026-07-14": "booked",
    "2026-07-16": "booked",
    "2026-07-18": "available",
    "2026-07-20": "available",
    "2026-07-22": "available",
    "2026-07-24": "booked",
    "2026-07-26": "booked",
    "2026-07-30": "booked",
}

def collect_customer_message(state):
  user_inquiry =  input('enter you inquiry :')
  return {
      "human_message": user_inquiry,

      'messages' : [HumanMessage(content = user_inquiry)]

  }

from langchain_core.tools import tool



@tool
def check_calendar(date : str):
  """Checks the availability status for a given date in the calendar."""
  print(f"Tool called with: {date}")  
  if date in calendar:
    return { 'status' : calendar[date]}
  else:
    return{'status' : 'not available'}

model_with_tools = model.bind_tools([check_calendar])
tool_node=ToolNode([check_calendar])

def khay_assistant(state):

  prompt = ChatPromptTemplate.from_messages([
      ('system' , '''you are a fashion designers assistant,her name is tailor khay,you will respond
                to messages asked by her customer,if its about things you dont know,say you dont know
              make sure you are nice and very polite
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

      elif i in ['book','appointment']:
        return {
          'intent': 'appointment'
      }


    else:
      return {
          'intent' : 'general'
      }
def book_appointment(state):
  message='the only date available for the date of july is 24 and 27'
  print(message)
  return{
      'ai_message' : message,
      'messages': [AIMessage (content= message)]
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
graph.add_node('book_appointment',book_appointment)
graph.add_node('pricing',pricing)
graph.add_node('intent_router',intent_router)
graph.add_node('continue_router', should_continue)
graph.add_node('tools',tool_node)
graph.add_edge(START,'collect_customer_message')
graph.add_edge('collect_customer_message' , 'intent_router')
graph.add_conditional_edges ('intent_router',
                lambda state : state['intent'],
                {'pricing' : 'pricing',
                'appointment': 'book_appointment',
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


graph.add_edge('book_appointment', 'continue_router')
graph.add_edge('pricing', 'continue_router')

app=graph.compile(checkpointer=memory)
app.invoke({ },
           config = {
               'configurable' : {
                   'thread_id' : 'customer_001'
               }
           })

