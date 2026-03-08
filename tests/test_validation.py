from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_category_tags_invalid_payload():
    response = client.post("/ai/category-tags", json={})
    assert response.status_code == 422


def test_proposals_invalid_payload():
    response = client.post("/ai/proposals", json={})
    assert response.status_code == 422