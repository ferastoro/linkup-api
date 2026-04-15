from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.profile import Profile
from schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from auth.jwt import verify_token
from typing import List

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileResponse, status_code=201)
def create_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    existing = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profil sudah ada")
    profile = Profile(**data.dict(), user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=List[ProfileResponse])
def get_all_profiles(db: Session = Depends(get_db)):
    return db.query(Profile).all()

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil tidak ditemukan")
    return profile

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil tidak ditemukan")
    if profile.user_id != user_id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{profile_id}", status_code=204)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil tidak ditemukan")
    if profile.user_id != user_id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")
    db.delete(profile)
    db.commit()