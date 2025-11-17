import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from app.models import question, answer

client = TestClient(app)


# Тестовая база данных
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_question(test_db):
    response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test question?"
    assert "id" in data
    assert "created_at" in data


def test_create_question_empty_text(test_db):
    response = client.post("/api/v1/questions/", json={"text": ""})
    assert response.status_code == 400


def test_get_questions(test_db):
    # Сначала создаем вопрос
    client.post("/api/v1/questions/", json={"text": "Test question?"})

    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "total" in data
    assert len(data["questions"]) == 1


def test_get_question_not_found(test_db):
    response = client.get("/api/v1/questions/999")
    assert response.status_code == 404