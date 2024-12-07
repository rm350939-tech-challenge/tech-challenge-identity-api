import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_root(client, monkeypatch):
    monkeypatch.setenv("DATABASE_MONGO_USER", "test_user")
    monkeypatch.setenv("DATABASE_MONGO_PASSWORD", "test_password")
    monkeypatch.setenv("DATABASE_MONGO_HOST", "test_host")
    monkeypatch.setenv("DATABASE_MONGO_DATABASE", "test_database")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"project": "Tech Challence - Fase 4"}
