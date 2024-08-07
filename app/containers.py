from dependency_injector import providers, containers

from app.modules.profile.services import ProfileService
from app.modules.profile.repositories import ProfileRepository
from .database import Database

class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    profile_repository = providers.Factory(
        ProfileRepository,
        session_factory=db.provided.session,
    )

    profile_service = providers.Factory(
        ProfileService,
        profile_repository=profile_repository,
    )
