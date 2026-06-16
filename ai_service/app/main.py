from fastapi import FastAPI
from schemas import AnswerResponse, QuestionRequest

app = FastAPI()


@app.get("/health")
def health():
    return {"messege": "OK"}


@app.post("/ask")
async def ask(question: QuestionRequest) -> AnswerResponse:
    return AnswerResponse(answer="echo")
