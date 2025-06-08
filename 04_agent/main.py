from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests

load_dotenv()
client = OpenAI()

def write_file(data: dict):
    path = data.get("path")
    content = data.get("content")
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"✅ Successfully wrote to {path}"
    except Exception as e:
        return f"❌ Failed to write to file: {e}"
    
def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city : str):
    url =  f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather" : get_weather,
    "run_command" : run_command,
    "write_file": write_file
}    

SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.
    - "write_file": Takes path as an input and write the code in the given path.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
    
    Example:
    User Query:Create a folder named Project-1 and inside the folder create an E-commerce website using HTML,CSS and Javascript
    Output: {{ "step": "plan", "content": "The user is interseted in building an E-commerce webiste using HTML , CSS And Javascript" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call run_command to create Project-1 Folder" }}
    Output: {{ "step": "action", "function": "run_command", "input": "mkdir Project-1" }}
    Output: {{ "step": "observe", "output": "Folder created successfully" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call run_command to create index.html , style.css and app.js files inside the Project-1 folder" }}
    Output: {{ "step": "action", "function": "run_command", "input": "touch index.html" }}
    Output: {{ "step": "observe", "output": "File created successfully" }}
    Output: {{ "step": "action", "function": "run_command", "input": "touch style.css" }}
    Output: {{ "step": "observe", "output": "File created successfully" }}
    Output: {{ "step": "action", "function": "run_command", "input": "touch app.js" }}
    Output: {{ "step": "observe", "output": "File created successfully" }}
    Output: {{ "step": "action","function":"write_file", "input": "HTML code" }}
    Output: {{ "step": "observe", "output": "Successfully wrote to index.html" }}
    Output: {{ "step": "action","function":"write_file", "input": "CSS code" }}
    Output: {{ "step": "observe", "output": "Successfully wrote to style.css" }}
    Output: {{ "step": "action","function":"write_file", "input": "js code" }}
    Output: {{ "step": "observe", "output": "Successfully wrote to app.js" }}
    Output: {{ "step": "output", "content": "Run the app in the browser" }}



"""

messages = [
    {"role" : "system" , "content" : SYSTEM_PROMPT}
    
]

while True:
    query = input("> ")
    messages.append({"role" : "user" , "content" : query})
    while True:
        response = client.chat.completions.create(
            model= "gpt-4.1",
            response_format={"type" : "json_object"},
            messages=messages
        )
        messages.append({"role":"assistant" , "content" : response.choices[0].message.content})
        parsed_response = json.loads(response.choices[0].message.content)
        
        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue
        
        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            print("💯", parsed_response)
            print(f"🛠️: Calling Tool: {tool_name} with input {tool_input}")
            
            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                messages.append({"role": "user" , "content" : json.dumps({"step" : "observe","output" : output })})
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break    