# flake8: noqa
from fastapi import FastAPI, Query, Path
from .queue.connection import queue
from .queue.worker import process_query
app = FastAPI()  # creates an app

@app.get('/') 
def chat():
    return { "status": "Server is up and running"}


@app.post('/chat')  # to invoke chat-  post call on app
def chat(
    query: str = Query(..., description="Chat Message")  # query in the form of str
):
    # insert query in Queue and then acknowledge the user than your query is being processed
    # using RQ library for queue
    job = queue.enqueue(process_query,query)  # return as job/infromation about query/message
    # user ko boldo your job recieved
    return {"status": "queued", "job_id": job.id}
    


@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    
    return {"result": result}