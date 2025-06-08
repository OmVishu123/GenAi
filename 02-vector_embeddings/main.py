from dotenv import load_dotenv
from openai import OpenAI
load_dotenv() # loads environment variable from .env file
client = OpenAI() # creating a client object to interact with the openAI API

text = "Dog chases cat"
response = client.embeddings.create( 
    
    model="text-embedding-3-small", #selecting a suitable model
    input= text
)

print("Vector Embeddings :",response)


