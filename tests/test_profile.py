import sys
import os
from unittest import mock
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models import Profile
from app.modules.profile.repositories import ProfileRepository

client = TestClient(app)

profile = {
    "id": 1,
    "img": "https://example.com/image.jpg",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "123-456-7890",
    "address": "123 Main St",
    "city": "Somewhere",
    "state": "CA",
    "zipcode": "12345",
    "available": True
}

def test_create_profile():
    """Test creating a new profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.create.return_value = Profile(**profile)

    with app.container.profile_repository.override(repository_mock):
        response = client.post("/profiles", json=profile)

    assert response.status_code == 200
    assert response.json()["first_name"] == "John"

def test_create_profile_missing_fields():
    """Test creating a new profile with missing fields."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.create.return_value = Profile(**profile)

    with app.container.profile_repository.override(repository_mock):
        response = client.post("/profiles", json={ "first_name": "John" })

    assert response.status_code == 422

def test_read_profile():
    """Test reading a profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.get.return_value = Profile(**profile)

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1")

    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


def test_read_profile_404():
    """Test reading a profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.get.return_value = None

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"

def test_update_profile():
    """Test updating"""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.update.return_value = Profile(**{ **profile, "first_name": "Jane" })

    with app.container.profile_repository.override(repository_mock):
        response = client.put("/profiles", json={ **profile, "first_name": "Jane"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"

def test_update_profile_404():
    """Test updating"""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.update.return_value = None

    with app.container.profile_repository.override(repository_mock):
        response = client.put("/profiles", json={ **profile, "first_name": "Jane"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"

def test_delete_profile():
    """Test deleting a profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.delete.return_value = Profile(**profile)

    with app.container.profile_repository.override(repository_mock):
        response = client.delete("/profiles/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_profile_404():
    """Test deleting a profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.delete.return_value = None

    with app.container.profile_repository.override(repository_mock):
        response = client.delete("/profiles/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"

def test_read_all_friends():
    """Test reading all profiles."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    friendOne = { **profile, "id": 2, "first_name": "Jane" }
    friendTwo = { **profile, "id": 3, "first_name": "Alice" }
    repository_mock.get_profile_friends.return_value = [Profile(**friendOne), Profile(**friendTwo)]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1/friends")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["first_name"] == "Jane"
    assert response.json()[1]["first_name"] == "Alice"
