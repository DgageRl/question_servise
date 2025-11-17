from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from .answer import AnswerResponse


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    answers: List[AnswerResponse] = []


class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse]
    total: int