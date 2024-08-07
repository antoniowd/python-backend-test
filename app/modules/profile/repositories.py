"""Profile Repository module."""
from sqlalchemy.orm import Session
from app.models import  Profile

class ProfileRepository:
    """SQLite repository."""
    def __init__(self):
        self.model = Profile

    def get(self, db: Session, id_: int) -> Profile | None:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id_).first()

    def list(self, db: Session):
        """List all records."""
        return db.query(self.model).all()

    def create(self, db: Session, item: Profile) -> Profile:
        """Create a new record."""
        new_item = self.model = item
        db.add(item)
        db.commit()
        db.refresh(new_item)
        return new_item

    def update(self, db: Session, id_: int, item: Profile) -> Profile | None:
        """Update a record by ID."""
        db.merge(item)
        db.commit()
        db.refresh(item)
        return self.get(db, id_)

    def delete(self, db: Session, id_: int) -> Profile | None:
        """Delete a record by ID."""
        item = self.get(db, id_)
        db.delete(item)
        db.commit()
        return item
