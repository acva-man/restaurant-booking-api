from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_table():
    response = client.post("/tables/", json={"name": "Table 1", "seats": 4, "location": "Window"})
    assert response.status_code == 200