from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login")
    assert response.status_code == 200
    data = response.json()
    print("Login success response:", data)

if __name__ == "__main__":
    test_login_success()
