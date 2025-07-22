# flake8: noqa


from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

import os
from dotenv import load_dotenv

# Load the .env file from /workspaces/GenAi
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not loaded. Check .env file or path.")

from openai import OpenAI
client = OpenAI(api_key=api_key)



# client = OpenAI()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)


async def process_query(query: str):
    print("Searching chunks", query)
    search_results  = vector_db.similarity_search(
    query=query
    )
    
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Loaction:{result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT  = f"""
    You are a Helpful AI assistant who answers user query based on the available context retreived from a PDF file along with page_contents and page number.
    
    You should only answer the user based on the following context and navigate the user to open the right page number to know more.
    
    Context: 
    {context}
"""

    chat_completion = client.chat.completions.create(
    model= "gpt-4.1",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user","content" : query}
    ]
)
    # save to DB
    print(f"🤖: {query}", chat_completion.choices[0].message.content, "\n\n\n" )
    return chat_completion.choices[0].message.content