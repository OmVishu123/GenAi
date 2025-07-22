from dotenv import load_dotenv
from openai import OpenAI
# will load the env(API)
load_dotenv()

# Presona - Based Prompting  
client = OpenAI()
# prompting
# Few-shot prompting (here we give example too)


SYSTEM_PROMPT ="""" 
    You are an AI expert in coding. You only know python and nothing else.
    
    
"""
