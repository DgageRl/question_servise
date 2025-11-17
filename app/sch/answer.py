from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AnswerBase(BaseModel):
    text: str
    user_id: str


class AnswerCreate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    created_at: datetime