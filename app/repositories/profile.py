"""Profile repository module."""
from sqlalchemy.orm import Session
from ..models import Profile
from .base import BaseRepository

class ProfileRepository(BaseRepository[Profile]):
    """Profile repository."""
    def __init__(self):
        super().__init__(Profile)

    def list_friends(self, db: Session, id_: int):
        # TODO: Implement this method
        pass
