from dependency_injector import providers, containers

from app.modules.profile.services import ProfileService
from app.modules.profile.repositories import ProfileRepository
from .database import Database

SQLALCHEMY_DATABASE_URL = "sqlite:///./storage.sqlite3"

class Container(containers.DeclarativeContainer):
    """Dependency injection container."""

    db = providers.Singleton(Database, db_url=SQLALCHEMY_DATABASE_URL)

    profile_repository = providers.Factory(
        ProfileRepository,
        session_factory=db.provided.session,
    )

    profile_service = providers.Factory(
        ProfileService,
        profile_repository=profile_repository,
    )
