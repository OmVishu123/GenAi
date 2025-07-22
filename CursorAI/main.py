from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    You are a helpful AI assistant.
    
    Working principle:
    1.Takes a query as an input by the user.
    2.Analyse the query.
    3.Think for the optimal solution
    4.Generate output.
    5.Verify the output
    6.Rectify if any mistake is present
    7.Give the final output as the result
    
    You follow the sequence "analyse" , "think" , "generate" , "verify" , "rectify" and finally "result" 
    Your respond should be JSON with fields : "step" and "content"
    
    Example:
    user query: create  a To-Do list using HTML, CSS and javascript
    Output: {{ "step": "analyse", "content": "The user is interseted in building a To-Do list using HTML , CSS And Javascript" }}
    Output: {{ "step": "plan", "content": "The user is interseted in building a To-Do list using HTML , CSS And Javascript" }}
    
"""

messages = [
    {"role": "system" ,"content": SYSTEM_PROMPT}
]
while True:
    query = input("> ")
    messages.append({"role" : "user" , "content" : query})
    while True:
        response = client.chat.completions.create(
            model= "gpt-4.1",
            response_format= {"type" : "json_object"},
            messages= messages,
            temperature=0.1
        )
        messages.append({"role": "assistant" , "content" : response.choices[0].message.content})
        parsed_message = json.loads(response.choices[0].message.content)
        print(parsed_message.get("role"), ">>", parsed_message.get("content"))
        if parsed_message.get("step") == "result":
            print("⭕ ", parsed_message.get("content"))  
            break
              