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

def test_read_all_profiles():
    """Test reading all the profiles."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    friendOne = { **profile, "id": 2, "first_name": "Jane" }
    friendTwo = { **profile, "id": 3, "first_name": "Alice" }
    repository_mock.get_all.return_value = [Profile(**friendOne), Profile(**friendTwo)]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["first_name"] == "Jane"
    assert response.json()[1]["first_name"] == "Alice"

def test_read_profile():
    """Test reading a profile."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.get.return_value = Profile(**profile)

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1")

    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


def test_read_profile_404():
    """Test reading a profile that does not exist."""
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
    """Test updating a profile that does not exist."""
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
    """Test deleting a profile that does not exists."""
    repository_mock = mock.Mock(spec=ProfileRepository)
    repository_mock.delete.return_value = None

    with app.container.profile_repository.override(repository_mock):
        response = client.delete("/profiles/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"

def test_read_all_friends():
    """Test reading all friends from a profile."""
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

def test_shorter_connection():
    """Test getting the shortest connection between two profiles."""
    repository_mock = mock.Mock(spec=ProfileRepository)

    profile1 = {**profile, "id": 1, "first_name": "Roberto"}
    profile2 = {**profile, "id": 2, "first_name": "Ana"}
    profile3 = {**profile, "id": 3, "first_name": "Juan"}
    profile4 = {**profile, "id": 4, "first_name": "Maykel"}
    profile5 = {**profile, "id": 5, "first_name": "Leo"}

    profiles = {
        1: [Profile(**profile2), Profile(**profile3)],
        2: [Profile(**profile1), Profile(**profile5)],
        3: [Profile(**profile1), Profile(**profile4)],
        4: [Profile(**profile3), Profile(**profile5)],
        5: [Profile(**profile2), Profile(**profile4)]
    }

    repository_mock.get_profile_friends.side_effect = lambda id_: profiles[id_]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1/shorter/5")

    assert response.status_code == 200
    assert response.json() == [2]

def test_shorter_connection_not_found():
    """Test a connection that does not exists."""
    repository_mock = mock.Mock(spec=ProfileRepository)

    profile2 = {**profile, "id": 2, "first_name": "Ana"}
    profile3 = {**profile, "id": 3, "first_name": "Juan"}

    profiles = {
        1: [Profile(**profile2), Profile(**profile3)],
        2: [Profile(**profile3)],
        3: [Profile(**profile2)],
        4: []
    }

    repository_mock.get_profile_friends.side_effect = lambda id_: profiles[id_]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1/shorter/4")

    assert response.status_code == 404
    assert response.json()["detail"] == "No connection found"

def test_shorter_connection_same_id():
    """Test connection with the same id."""
    repository_mock = mock.Mock(spec=ProfileRepository)

    profile2 = {**profile, "id": 2, "first_name": "Ana"}
    profile3 = {**profile, "id": 3, "first_name": "Juan"}

    profiles = {
        1: [Profile(**profile2), Profile(**profile3)],
    }

    repository_mock.get_profile_friends.side_effect = lambda id_: profiles[id_]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1/shorter/1")

    assert response.status_code == 200
    assert response.json() == [1]

def test_shorter_connection_direct_one():
    """Test a direct connection."""
    repository_mock = mock.Mock(spec=ProfileRepository)

    profile2 = {**profile, "id": 2, "first_name": "Ana"}

    profiles = {
        1: [Profile(**profile2)],
        2: []
    }

    repository_mock.get_profile_friends.side_effect = lambda id_: profiles[id_]

    with app.container.profile_repository.override(repository_mock):
        response = client.get("/profiles/1/shorter/2")

    assert response.status_code == 200
    assert response.json() == [2]
