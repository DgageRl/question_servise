from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from typing import List, Optional

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    return db.query(Question).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()

def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int) -> bool:
    db_question = get_question(db, question_id)
    if db_question:
        db.delete(db_question)
        db.commit()
        return True
    return False

def get_questions_count(db: Session) -> int:
    return db.query(Question).count()