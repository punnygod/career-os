from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.role import Role
from pydantic import BaseModel


router = APIRouter(prefix="/api/roles", tags=["roles"])


class RoleResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    """Get all available roles."""
    roles = db.query(Role).filter(Role.is_active == 1).all()
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID."""
    role = db.query(Role).filter(Role.id == role_id, Role.is_active == 1).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
