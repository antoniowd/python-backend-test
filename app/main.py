from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schema, database
from .services.profile import ProfileService

app = FastAPI()

# Dependency
def get_db():
    """Get database session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: Solve deprecation
@app.on_event("startup")
def startup_event():
    """Startup event."""
    database.init_db()

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to your profile manager!"}

@app.post("/profiles", response_model=schema.Profile)
def create_profile(profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """Create a new profile."""
    return ProfileService(db).create(models.Profile(**profile.model_dump()))

@app.get("/profiles", response_model=List[schema.Profile])
def list_profiles(db: Session = Depends(get_db)):
    """List all profiles."""
    return ProfileService(db).list()

@app.get("/profiles/{id_}", response_model=schema.Profile)
def get_profile(id_: int, db: Session = Depends(get_db)):
    """Get a single profile by ID."""
    profile = ProfileService(db).get(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/profiles/{id_}", response_model=schema.Profile)
def update_profile(id_: int, profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """Update a profile by ID."""
    profile = ProfileService(db).update(id_, models.Profile(**profile.model_dump()))
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.delete("/profiles/{id_}", response_model=schema.Profile)
def delete_profile(id_: int, db: Session = Depends(get_db)):
    """Delete a profile by ID."""
    profile = ProfileService(db).delete(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
