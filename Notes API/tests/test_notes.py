import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh database tables for each test and drop them afterwards."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "documentation" in data


def test_create_note():
    payload = {"title": "Test Title", "content": "Test Content"}
    response = client.post("/notes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Title"
    assert data["content"] == "Test Content"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_note_invalid_payload():
    # Empty title should fail validation
    payload = {"title": "", "content": "Test Content"}
    response = client.post("/notes/", json=payload)
    assert response.status_code == 422


def test_get_all_notes():
    # Create two notes first
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})

    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Note 1"
    assert data[1]["title"] == "Note 2"


def test_get_note_by_id():
    create_resp = client.post("/notes/", json={"title": "Specific Note", "content": "Specific Content"})
    note_id = create_resp.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Specific Note"


def test_get_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note with ID 999 not found"


def test_update_note():
    create_resp = client.post("/notes/", json={"title": "Old Title", "content": "Old Content"})
    note_id = create_resp.json()["id"]

    update_payload = {"title": "New Title", "content": "New Content"}
    response = client.put(f"/notes/{note_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"


def test_update_note_partial():
    create_resp = client.post("/notes/", json={"title": "Title", "content": "Content"})
    note_id = create_resp.json()["id"]

    update_payload = {"title": "Only Title Updated"}
    response = client.put(f"/notes/{note_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Only Title Updated"
    assert data["content"] == "Content"


def test_update_note_not_found():
    response = client.put("/notes/999", json={"title": "Title"})
    assert response.status_code == 404


def test_delete_note():
    create_resp = client.post("/notes/", json={"title": "Delete Me", "content": "Delete Content"})
    note_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/notes/{note_id}")
    assert delete_resp.status_code == 204

    # Verify it is no longer returned
    get_resp = client.get(f"/notes/{note_id}")
    assert get_resp.status_code == 404


def test_delete_note_not_found():
    response = client.delete("/notes/999")
    assert response.status_code == 404
