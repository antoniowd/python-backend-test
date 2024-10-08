"""Database module."""
from contextlib import contextmanager

from app.models import Base
from sqlalchemy import create_engine, orm

class Database:
    """Database class."""
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def create_database(self):
        """Create the database."""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def session(self):
        """Provide a transactional scope around a series of operations."""
        session: orm.Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()
