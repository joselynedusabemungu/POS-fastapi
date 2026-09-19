import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"

from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "role": "Cashier",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user(client, auth_headers):
    response = client.post(
        "/users/",
        json={
            "username": "seconduser",
            "password": "secondpassword",
            "role": "Cashier",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()
