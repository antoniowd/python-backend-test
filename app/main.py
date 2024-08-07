from fastapi import FastAPI
from .containers import Container
from .modules.profile import routes as profile_routes

def create_app() -> FastAPI:
    """Create the application."""
    _app = FastAPI()
    container = Container()

    container.wire(modules=[profile_routes])

    db = container.db()
    db.create_database()

    _app.container = container

    _app.include_router(profile_routes.router)
    return _app

app = create_app()
