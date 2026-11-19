import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_chat_success(client):
    response = client.post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert response.status_code == 200
    assert "response" in response.get_json()


def test_empty_message(client):
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 400


def test_missing_message(client):
    response = client.post("/api/chat", json={})
    assert response.status_code == 400


def test_invalid_json(client):
    response = client.post("/api/chat", data="это не json", content_type="application/json")
    assert response.status_code == 400


def test_too_long_message(client):
    response = client.post("/api/chat", json={"message": "a" * 1001})
    assert response.status_code == 400


def test_wrong_input_type(client):
    response = client.post("/api/chat", json={"message": 12345})
    assert response.status_code == 400
