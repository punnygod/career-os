from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

from database import get_db
from models.user import User
from models.assessment import Assessment
from config import settings


router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str


class SaveAssessmentRequest(BaseModel):
    session_id: str


def hash_password(password: str) -> str:
    """Hash a password, truncating to 72 bytes if needed."""
    # Bcrypt has a 72-byte limit that passlib triggers an error for
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash, truncating plain password if needed."""
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


@router.post("/register", response_model=AuthResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(request.password)
    user = User(
        email=request.email,
        hashed_password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )


@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user.
    """
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )


@router.post("/save-assessment")
def save_assessment(
    request: SaveAssessmentRequest,
    user_id: int,  # This would come from JWT token in production
    db: Session = Depends(get_db)
):
    """
    Link an anonymous assessment to a user account.
    """
    # Find assessment by session_id
    assessment = db.query(Assessment).filter(
        Assessment.session_id == request.session_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Link to user
    assessment.user_id = user_id
    assessment.session_id = None  # Clear session ID
    
    db.commit()
    
    return {"message": "Assessment saved successfully"}
