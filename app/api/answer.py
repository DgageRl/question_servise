from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import answer as crud_answer
from app.schemas.answer import AnswerCreate, AnswerResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/questions/{question_id}/answers/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    if not answer.text or not answer.text.strip():
        raise HTTPException(status_code=400, detail="Answer text cannot be empty")

    if not answer.user_id or not answer.user_id.strip():
        raise HTTPException(status_code=400, detail="User ID cannot be empty")

    try:
        db_answer = crud_answer.create_answer(db=db, answer=answer, question_id=question_id)
        if db_answer is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return db_answer
    except Exception as e:
        logger.error(f"Error creating answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/answers/{answer_id}", response_model=AnswerResponse)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud_answer.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer


@router.delete("/answers/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    success = crud_answer.delete_answer(db, answer_id=answer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"message": "Answer deleted successfully"}