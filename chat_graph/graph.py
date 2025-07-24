# flake8: noqa
from dotenv import load_dotenv
from typing_extensions import TypedDict
from openai import OpenAI
from typing import Annotated
from langgraph.graph import StateGraph, START ,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
llm = init_chat_model(model_provider="openai" , model="gpt-4.1")
    
def chat_bot(state : State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START , "chat_bot")
graph_builder.add_edge("chat_bot" , END)
graph = graph_builder.compile()
   
   
   #create a graph with checkpointer using function
def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer= graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer


def main():
    # create a thread_id
    config = {"configurable": {"thread_id":"1"}}
    # if we change the thread id , it will create another space to store the states
    
    #create a url-- syntax -> mongodb://<username>:<pass>@<host>:<port>
    DB_URI = "mongodb://admin:admin@mongodb:27017"
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        
        query = input("> ")
        
        response = graph_with_mongo.invoke({"messages" : [{"role" :"user" , "content":query}]},config)

        print(response)
main()    