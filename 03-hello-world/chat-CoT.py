#Chain-Of-Thought (CoT) Prompting
from dotenv import load_dotenv
from openai import OpenAI
import json
# will load the env(API)
load_dotenv()

client = OpenAI()
# prompting
# Chain Of Thought : The model is encouraged to break down reasoning step by step before arriving to the conclusion



SYSTEM_PROMPT ="""" 
    You are an helpful AI assistant who is specialized in resolving user query.
    For the given user input , analyse the input and break down the problem step by step.
    
    The steps are:
        You get an user input,
        You analyse,
        You think,
        You think again,
        and think for several times,
        before arriving to the answer.
    
    Follow the steps in sequence that is "analyse",  "think", "output", "validate" and finally "result".    
    
    Rules:
    1. Follow the strict JSON output per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query.
    
    Output Format:
    {{"step": "string","content": "string"}}
    
    Example:
    Input: What is 2 + 2 * 5/ 3
    
    Output:{{"step": "analyse", "content": "Alright! The user is interseted in maths query and he is asking a basic arithmatic operation"  }}
    
    Output:{{"step": "think", "content": "To perform this addtion , I must use BODMAS rule."  }}
    
    Output:{{"step": "validate", "content": "Correct, using BODMAS is the right approach here."  }}
    
    Output:{{"step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.6666"  }}
    
    Output:{{"step": "validate", "content": "Correct, using BODMAS division must be performed"  }}
    
    Output:{{"step" : "think", "content": "Now, as I solved 5 / 3 the eqaution looks like 2 + 2 * 1.6666667"  }}
    
    Output:{{"step": "validate", "content": "Yes, the eqaution is absolutely correct."  }}
    
    Output:{{"step" : "think", "content": "Now,according to rule of BODMAS solve the multiplication that is 2 * 1.666667 which is 3.3333333"  }}
    and so on...
    
    
    
    
"""
# response = client.chat.completions.create(
#     model="gpt-4.1-mini",  # faster but inaccurate (cheap)
#     response_format={"type":"json_object"},
#     messages=[
#         {"role": "system","content" : SYSTEM_PROMPT},
#         {"role" : "user" ,"content" : "What is 5 / 2 * 3 to the power 4 "},
#         {"role" : "assistant" ,"content" : json.dumps(  {"step": "analyse", "content": "The user is asking to evaluate a mathematical expression: 5 divided by 2, then multiplied by 3 raised to the power of 4."} )} ,# json -> python
#         {"role" : "assistant" ,"content" : json.dumps(  {"step": "think", "content": "To solve 5 / 2 * 3^4, first calculate the exponentiation 3^4, then perform the division and multiplication from left to right."} )}, # json -> python
#         {"role" : "assistant" ,"content" : json.dumps(  {"step": "output", "content": "3 to the power 4 is 81. Now, 5 / 2 = 2.5, and then 2.5 * 81 = 202.5."} )}, # json -> python
#         {"role" : "assistant" ,"content" : json.dumps(  {"step": "validate", "content": "Calculations are accurate: 3^4 = 81, then 5 / 2 = 2.5, multiplied by 81 equals 202.5."})} # json -> python
  
#     ]
# )
# print("\n\n🤖",response.choices[0].message.content,"\n\n")


messages = [
    {"role" : "system" , "content" : SYSTEM_PROMPT}
    
]

query = input("> ")
messages.append({"role": "user" , "content" : query})

while True:
    response = client.chat.completions.create(
        model ="gpt-4.1",
        response_format="json",
        messages=messages
    )
    messages.append({"role" : "assistant" ,"content" : response.choices[0].message.content })
    parsed_response = json.loads(response.choices[0].message.content)
    
    
    # calling gpt-4.1-mini for validate response( multi model based)
    if parsed_response.get("step") == "validate":
        # make the Claude API/ model (gpt-4.1-mini) API call and append the result as validate
        print("          🧠:" , parsed_response.get("content"))
        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            response_format="json",
            messages=messages
            
        )
        
        messages.append({"role": "assistant" ,"content" : response.choices[0].message.content })
        continue
        
    
    if parsed_response.get("step") != "result":
        print("          🧠:" , parsed_response.get("content"))
        continue
    
    
    print("🤖:" , parsed_response.get("content"))
    break
