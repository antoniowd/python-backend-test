from fastapi import FastAPI
from . import database
from .modules.profile.routes import router as profile_router

def create_app() -> FastAPI:
    """Create the application."""
    app = FastAPI()
    app.include_router(profile_router)
    return app

app = create_app()

# TODO: Solve deprecation
@app.on_event("startup")
def startup_event():
    """Startup event."""
    database.init_db()
