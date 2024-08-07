"""Profile service module."""
from typing import List
from sqlalchemy.orm import Session
from .repositories import ProfileRepository
from app.models import Profile

class ProfileService:
    """Profile service."""
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProfileRepository()

    def get(self, id_: int) -> Profile | None:
        """Get a single profile by ID."""
        return self.repo.get(self.db, id_)

    def list(self) -> List[Profile]:
        """List all profiles."""
        return self.repo.list(self.db)

    def create(self, item: Profile) -> Profile:
        """Create a new profile."""
        return self.repo.create(self.db, item)

    def update(self, id_: int, item: Profile) -> Profile | None:
        """Update a profile by ID."""
        return self.repo.update(self.db, id_, item)

    def delete(self, id_: int) -> Profile | None:
        """Delete a profile by ID."""
        return self.repo.delete(self.db, id_)
