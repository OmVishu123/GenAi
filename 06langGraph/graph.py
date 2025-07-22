# flake8: noqa
from dotenv import load_dotenv
from typing_extensions import TypedDict
from openai import OpenAI
from langgraph.graph import StateGraph, START ,END
load_dotenv()
client = OpenAI()
# creating a State
class State(TypedDict):
    query : str
    llm_result: str | None
    
# create a node    
SYSTEM_PROMPT = '''
    You are a helpful AI assistant for coding.
    You generate a simple code each time as a result after assisting the user.
    Example:
        User :"Hello"
        Output : {"role" : "assistant" , "content" : `Hi , How can I assist you? Do you know the code to print a fibonnaci series ? Here you go!!
        def fib(n):
            if n==0 or n==1:
                return 1
            else:
                return fib(n-1) + fib(n-2)            
         
        `}
        
'''
messages = [
    {"role" :"system" , "content" :SYSTEM_PROMPT}
]
def chat_bot(state :State):
    query = state["query"]
    messages.append({"role" :"user" , "content" :query})
    chat_completions =  client.chat.completions.create(
        model= "gpt-4.1-mini",
        messages = messages
        
    )
    result = chat_completions.choices[0].message.content
    state["llm_result"] = result
    
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_edge(START , "chat_bot")
graph_builder.add_edge( "chat_bot", END)   # graph = START -> Chat_bot -> END

# now build the graph
graph = graph_builder.compile()






def main():
    user = input("> ")
    
    #Invoke the graph - to invoke the grsph we need a state
    
    _state = {
        "query" : user,
        "llm_result" :None
    }
    
    graph_result = graph.invoke(_state)
    
    print("graph_result", graph_result)
     
main()  