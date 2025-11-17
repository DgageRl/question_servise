from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate
from typing import List, Optional


def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    return db.query(Answer).filter(Answer.id == answer_id).first()


def create_answer(db: Session, answer: AnswerCreate, question_id: int) -> Optional[Answer]:
    # Проверяем существование вопроса
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return None

    db_answer = Answer(
        text=answer.text,
        user_id=answer.user_id,
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int) -> bool:
    db_answer = get_answer(db, answer_id)
    if db_answer:
        db.delete(db_answer)
        db.commit()
        return True
    return False


def get_answers_by_question(db: Session, question_id: int) -> List[Answer]:
    return db.query(Answer).filter(Answer.question_id == question_id).all()