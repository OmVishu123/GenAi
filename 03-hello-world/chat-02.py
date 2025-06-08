from dotenv import load_dotenv
from openai import OpenAI
# will load the env(API)
load_dotenv()

client = OpenAI()
# prompting
# Few-shot prompting (here we give example too)


SYSTEM_PROMPT ="""" 
    You are an AI expert in coding. You only know python and nothing else.
    You help user in solving their python doubts only and nothing else.
    If user tried to ask something else apart from python you can just roast them.
    
    Examples:
    User : How to make a Tea?
    Assistant: What makes you think I am a chef?
    
    Examples:
    User: How to write a function in python?
    Assistant: def func(x:int)->int:
                pass #logic of the function
    
"""
response = client.chat.completions.create(
    model="gpt-4.1-mini",  # faster but inaccurate (cheap)
    messages=[
        {"role": "system","content" : SYSTEM_PROMPT},
        
        {"role":"user" ,"content" : "Hey, my name is Om",},  # doesn't have access to the real time data,
        
        #when we are chatting , then we always have to send an array
        
        # {"role" : "assistant", "content": "Hi Om! How can I assist you today?"},
        
        # {"role" : "user","content":"Whats my name?"}
        
    ]
)
print(response.choices[0].message.content)