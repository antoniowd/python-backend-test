"""Base repository module"""
from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from ..models import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository."""
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id_: int) -> ModelType | None:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id_).first()

    # TODO: Implement pagination
    def list(self, db: Session):
        """List all records."""
        return db.query(self.model).all()

    def create(self, db: Session, item: ModelType) -> ModelType:
        """Create a new record."""
        new_item = self.model(**item)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    def update(self, db: Session, id_: int, item: ModelType) -> ModelType | None:
        """Update a record by ID."""
        db.merge(item)
        db.commit()
        db.refresh(item)
        return self.get(db, id_)

    def delete(self, db: Session, id_: int) -> ModelType | None:
        """Delete a record by ID."""
        item = self.get(db, id_)
        db.delete(item)
        db.commit()
        return item
