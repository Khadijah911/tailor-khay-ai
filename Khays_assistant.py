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

  next_action : str
  messages : Annotated[list,add_messages]

memory=MemorySaver()
def collect_customer_message(state):
  user_inquiry =  input('enter you inquiry :')
  return {
      "human_message": user_inquiry,

      'messages' : [HumanMessage(content = user_inquiry)]

  }

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

  response =model.invoke(message)
  print(response.content)
  return {
      'ai_message' : response.content,
      'messages' : [AIMessage(content = response.content)

  ]

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
  if 'bye' in state['human_message'].lower().split():

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
graph.add_node('should_continue', should_continue)
graph.add_edge(START,'collect_customer_message')
graph.add_edge('collect_customer_message' , 'intent_router')
graph.add_conditional_edges ('intent_router',
                lambda state : state['intent'],
                {'pricing' : 'pricing',
                'appointment': 'book_appointment',
                'general' : 'khay_assistant'
                 })
graph.add_conditional_edges('should_continue',
                            lambda state : state['next_action'],
                            {'continue' : 'collect_customer_message',
                             'stop' : END}
                            )

graph.add_edge('book_appointment', 'should_continue')
graph.add_edge('pricing', 'should_continue')
graph.add_edge('khay_assistant', 'should_continue')
app=graph.compile(checkpointer=memory)
app.invoke({ },
           config = {
               'configurable' : {
                   'thread_id' : 'customer_001'
               }
           })



