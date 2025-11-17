from sqlalchemy.orm import Session
from app.models import answer as models
from app.models import question as question_models
from app.schemas import answer as schemas
from typing import List, Optional


def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()


def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int) -> Optional[models.Answer]:
    # Проверяем существование вопроса
    question = db.query(question_models.Question).filter(question_models.Question.id == question_id).first()
    if not question:
        return None

    db_answer = models.Answer(
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


def get_answers_by_question(db: Session, question_id: int) -> List[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()