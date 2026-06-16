from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    lesson_content: str


class AnswerResponse(BaseModel):
    answer: str
