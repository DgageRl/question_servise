from fastapi import FastAPI
from app.database import engine
from app.models import question, answer
from app.api import questions, answers
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


question.Base.metadata.create_all(bind=engine)
answer.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Q&A Service API",
    description="API сервис для вопросов и ответов",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(questions.router, prefix="/api/v1", tags=["questions"])
app.include_router(answers.router, prefix="/api/v1", tags=["answers"])

@app.get("/")
async def root():
    return {"message": "Q&A Service API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}