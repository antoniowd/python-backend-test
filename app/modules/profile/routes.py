from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from app import schema, models
from .services import ProfileService
from app.containers import Container

router = APIRouter()

@router.post("/profiles", response_model=schema.Profile)
@inject
def create_profile(
    profile: schema.ProfileCreate,
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """Create a new profile."""
    return profile_service.create(models.Profile(**profile.model_dump()))

@router.get("/profiles", response_model=List[schema.Profile])
@inject
def get_all_profiles(
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """List all profiles."""
    return profile_service.get_all()

@router.get("/profiles/{id_}", response_model=schema.Profile)
@inject
def get_profile(
    id_: int,
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """Get a single profile by ID."""
    profile = profile_service.get(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/profiles/{id_}/friends", response_model=List[schema.Profile])
@inject
def get_profile_friends(
    id_: int,
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """Get all friends from a profile ID."""
    return profile_service.get_profile_friends(id_)

@router.put("/profiles", response_model=schema.Profile)
@inject
def update_profile(
    profile: schema.ProfileUpdate,
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """Update a profile by ID."""
    profile = profile_service.update(models.Profile(**profile.model_dump()))
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.delete("/profiles/{id_}", response_model=schema.Profile)
@inject
def delete_profile(
    id_: int,
    profile_service: ProfileService = Depends(Provide[Container.profile_service])
):
    """Delete a profile by ID."""
    profile = profile_service.delete(id_)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
