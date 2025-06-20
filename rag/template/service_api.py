from fastapi import FastAPI, Request
from pydantic import BaseModel
from mcp_interface import get_answer

app = FastAPI()

class QARequest(BaseModel):
    question: str

@app.post("/qa")
def qa_endpoint(req: QARequest):
    answer = get_answer(req.question)
    return {"answer": answer}