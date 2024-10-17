from fastapi.testclient import TestClient

# app works on specific environment variable, this is set in conftest.py
from app.main import app

client = TestClient(app)


def test_get_all_content(monkeypatch):
    monkeypatch.setattr(
        "app.routers.public.preditor._authenticate_preditor", lambda x: None
    )
    response = client.get("api/static-content")
    assert response.status_code == 200
