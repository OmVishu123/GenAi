import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()

st.set_page_config(page_title="Smart AI", layout="wide")
tab1, tab2 = st.tabs(["\U0001F4E4 Upload PDF", "\U0001F4AC Ask Questions"])
#  upload and embed
with tab1:
    st.title("Smart AI")
    st.subheader("\U0001F4E4 Upload PDF")
    uploaded_file = st.file_uploader("Upload your file(pdf or site link)", type=None)

    if uploaded_file is not None:
        # read file in bytes
        with st.spinner("Uploading and Processing your pdf..."):
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
            
            if file_name.endswith(".pdf"):
                with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file_bytes)
                    tmp_file_path = tmp_file.name

                # Load and split documents
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                    #chunking
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size = 1000,
                    chunk_overlap = 400
                )        
                split_docs = text_splitter.split_documents(documents=docs)
                
                #vector embedding
                embedding_model = OpenAIEmbeddings(
                    model= "text-embedding-3-large"
                    
                )
                
                vector_store = QdrantVectorStore.from_documents(
                    documents=split_docs,
                    url="http://localhost:6333",
                    collection_name= "RAG_Project",
                    embedding=embedding_model
                )
                st.success("File uploaded successfully!")
            else:
                st.warning("Upload a file first")
            
with tab2:

    client = OpenAI()
    #vector embeddings
    embedding_model = OpenAIEmbeddings(
        model = "text-embedding-3-large"
    )

    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="RAG_Project",
        embedding= embedding_model
    )
    st.subheader("\U0001F4AC ASK AI")
    #Take user input
    query = st.text_input("Ask Anything")
    if query:
    #vector similarity search in DB
        search_result = vector_db.similarity_search(
            query=query
        )

        context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Loaction:{result.metadata['source']}" for result in search_result])
        SYSTEM_PROMPT  = f"""
            You are a Helpful AI assistant who answers user query based on the available context retreived from a PDF file along with page_contents and page number.
            
            You should only answer the user based on the following context and navigate the user to open the right page number to know more.
            
            Context: 
            {context}
        """

        messages = [
            {"role":"system", "content":SYSTEM_PROMPT},
            {"role":"user","content":query}
            ]

        chat_completion = client.chat.completions.create(
                model= "gpt-4.1-mini",
                messages=messages,
                temperature=0
                
        )
        st.markdown("## Result")
        st.write(chat_completion.choices[0].message.content)

                