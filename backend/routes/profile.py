from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import get_db
from models.user_profile import UserProfile
from models.stack import Stack
from models.certificate import Certificate

router = APIRouter(prefix="/api/profile", tags=["profile"])

class ProfileUpdate(BaseModel):
    role: Optional[str] = None
    primary_stack: Optional[str] = None
    secondary_stack: Optional[str] = None
    certifications: Optional[List[str]] = None
    experience_years: Optional[float] = None

@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        # Create empty profile if not exists
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile.to_dict()

@router.post("/{user_id}")
def update_profile(user_id: int, request: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
    
    if request.role is not None:
        profile.role = request.role
    if request.primary_stack is not None:
        profile.primary_stack = request.primary_stack
    if request.secondary_stack is not None:
        profile.secondary_stack = request.secondary_stack
    if request.certifications is not None:
        profile.certifications = request.certifications
    if request.experience_years is not None:
        profile.experience_years = request.experience_years
        
    db.commit()
    db.refresh(profile)
    return profile.to_dict()

@router.get("/meta/stacks")
def get_stacks(db: Session = Depends(get_db)):
    stacks = db.query(Stack).all()
    return [s.to_dict() for s in stacks]

@router.get("/meta/certificates")
def get_certificates(db: Session = Depends(get_db)):
    certs = db.query(Certificate).all()
    return [c.to_dict() for c in certs]
