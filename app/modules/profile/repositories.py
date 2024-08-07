"""Profile Repository module."""
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.models import  Profile, Friends

class ProfileRepository:
    """SQLite repository."""
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get(self, id_: int) -> Profile | None:
        """Get a single record by ID."""
        with self.session_factory() as db:
            return db.query(Profile).filter(Profile.id == id_).first()

    def get_all(self):
        """List all records."""
        with self.session_factory() as db:
            return db.query(Profile).all()

    def get_profile_friends(self, id_: int):
        """Get all friends from a profile id."""
        with self.session_factory() as db:
            return db.query(Profile).join(
                Friends, Profile.id == Friends.friend_id
            ).filter(Friends.profile_id == id_).all()

    def create(self, item: Profile) -> Profile:
        """Create a new record."""
        with self.session_factory() as db:
            db.add(item)
            db.commit()
            db.refresh(item)
            return item

    def update(self, item: Profile) -> Profile | None:
        """Update a record by ID."""
        with self.session_factory() as db:
            db.merge(item)
            db.commit()
            return item

    def delete(self, id_: int) -> Profile | None:
        """Delete a record by ID."""
        with self.session_factory() as db:
            item = self.get(id_)
            db.delete(item)
            db.commit()
            return item
