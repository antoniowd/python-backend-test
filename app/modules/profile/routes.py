from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app import schema, models
from app.database import get_db
from .services import ProfileService

router = APIRouter()

@router.post("/profiles", response_model=schema.Profile)
def create_profile(profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """Create a new profile."""
    return ProfileService(db).create(models.Profile(**profile.model_dump()))

@router.get("/profiles", response_model=List[schema.Profile])
def list_profiles(db: Session = Depends(get_db)):
    """List all profiles."""
    return ProfileService(db).list()

@router.get("/profiles/{id_}", response_model=schema.Profile)
def get_profile(id_: int, db: Session = Depends(get_db)):
    """Get a single profile by ID."""
    profile = ProfileService(db).get(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profiles/{id_}", response_model=schema.Profile)
def update_profile(id_: int, profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """Update a profile by ID."""
    profile = ProfileService(db).update(id_, models.Profile(**profile.model_dump()))
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.delete("/profiles/{id_}", response_model=schema.Profile)
def delete_profile(id_: int, db: Session = Depends(get_db)):
    """Delete a profile by ID."""
    profile = ProfileService(db).delete(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
