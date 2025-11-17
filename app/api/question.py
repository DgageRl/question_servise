from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import question as crud_question
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionListResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/questions/", response_model=QuestionListResponse)
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        questions = crud_question.get_questions(db, skip=skip, limit=limit)
        total = crud_question.get_questions_count(db)
        return {"questions": questions, "total": total}
    except Exception as e:
        logger.error(f"Error fetching questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/questions/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    if not question.text or not question.text.strip():
        raise HTTPException(status_code=400, detail="Question text cannot be empty")

    try:
        return crud_question.create_question(db=db, question=question)
    except Exception as e:
        logger.error(f"Error creating question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud_question.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    success = crud_question.delete_question(db, question_id=question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}