"""Profile service module."""
from typing import List
from .repositories import ProfileRepository
from app.models import Profile

class ProfileService:
    """Profile service."""
    def __init__(self, profile_repository: ProfileRepository):
        self.repo = profile_repository

    def get(self, id_: int) -> Profile | None:
        """Get a single profile by ID."""
        return self.repo.get(id_)

    def get_all(self) -> List[Profile]:
        """List all profiles."""
        return self.repo.get_all()

    def get_profile_friends(self, id_) -> List[Profile]:
        """List all profiles."""
        return self.repo.get_profile_friends(id_)

    def create(self, item: Profile) -> Profile:
        """Create a new profile."""
        return self.repo.create(item)

    def update(self, item: Profile) -> Profile | None:
        """Update a profile by ID."""
        return self.repo.update(item)

    def delete(self, id_: int) -> Profile | None:
        """Delete a profile by ID."""
        return self.repo.delete(id_)
