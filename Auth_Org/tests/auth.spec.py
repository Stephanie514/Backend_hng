
### Step 8: Testing
1. **Writing tests in `tests/auth.spec.py`:**
```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[database.get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_register_user(client):
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "password",
        "phone": "1234567890"
    })
    assert response.status_code == 201
    assert response.json()["data"]["user"]["email"] == "johndoe@example.com"

def test_login_user(client):
    response = client.post("/auth/login", data={
        "username": "johndoe@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_missing_fields_registration(client):
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "password": "password"
    })
    assert response.status_code == 422
    assert response.json()["errors"][0]["field"] == "email"

def test_duplicate_email_registration(client):
    client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "password",
        "phone": "1234567890"
    })
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "password",
        "phone": "1234567890"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
