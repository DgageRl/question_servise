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


def test_create_answer():
    # Сначала создаем вопрос
    question_response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = question_response.json()["id"]

    # Создаем ответ
    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test answer"
    assert data["user_id"] == "user123"
    assert data["question_id"] == question_id


def test_create_answer_invalid_question():
    response = client.post(
        "/api/v1/questions/999/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    assert response.status_code == 404


def test_create_answer_empty_text():
    question_response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "", "user_id": "user123"}
    )
    assert response.status_code == 400


def test_get_answer():
    # Создаем вопрос и ответ
    question_response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    answer_id = answer_response.json()["id"]

    # Получаем ответ
    response = client.get(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == answer_id
    assert data["text"] == "Test answer"


def test_delete_answer():
    # Создаем вопрос и ответ
    question_response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    answer_id = answer_response.json()["id"]

    # Удаляем ответ
    response = client.delete(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 200

    # Проверяем, что ответ удален
    response = client.get(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 404