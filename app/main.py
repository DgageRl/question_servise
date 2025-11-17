from fastapi import FastAPI
from app.database import engine
from app.models.question import Question
from app.models.answer import Answer
from app.api.questions import router as questions_router
from app.api.answers import router as answers_router
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание таблиц
Question.metadata.create_all(bind=engine)

app = FastAPI(
    title="Q&A Service API",
    description="API сервис для вопросов и ответов",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(questions_router, prefix="/api/v1", tags=["questions"])
app.include_router(answers_router, prefix="/api/v1", tags=["answers"])

@app.get("/")
async def root():
    return {"message": "Q&A Service API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}