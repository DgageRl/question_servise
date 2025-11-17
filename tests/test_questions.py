import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models.question import Question
from app.models.answer import Answer

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=engine)


def test_create_question():
    response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test question?"
    assert "id" in data
    assert "created_at" in data


def test_create_question_empty_text():
    response = client.post("/api/v1/questions/", json={"text": ""})
    assert response.status_code == 400


def test_get_questions():
    # Сначала создаем вопрос
    client.post("/api/v1/questions/", json={"text": "Test question?"})

    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "total" in data
    assert len(data["questions"]) == 1


def test_get_question_not_found():
    response = client.get("/api/v1/questions/999")
    assert response.status_code == 404


def test_delete_question():
    # Создаем вопрос
    response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = response.json()["id"]

    # Удаляем вопрос
    response = client.delete(f"/api/v1/questions/{question_id}")
    assert response.status_code == 200

    # Проверяем, что вопрос удален
    response = client.get(f"/api/v1/questions/{question_id}")
    assert response.status_code == 404