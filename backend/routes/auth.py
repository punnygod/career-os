from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import secrets
from passlib.context import CryptContext
from jose import JWTError, jwt

from database import get_db
from models.user import User
from models.assessment import Assessment
from config import settings


router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


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


class SocialLoginRequest(BaseModel):
    """Payload for social (Google/GitHub) login/signup."""

    provider: str
    email: EmailStr
    name: Optional[str] = None


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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the currently authenticated user from a bearer JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
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
    assessment.user_id = current_user.id
    assessment.session_id = None  # Clear session ID
    
    db.commit()
    
    return {"message": "Assessment saved successfully"}


@router.post("/social-login", response_model=AuthResponse)
def social_login(
    request: SocialLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login or sign up a user using a social provider (Google/GitHub).

    The frontend is responsible for verifying the identity with the provider
    and sending a trusted email address here. We treat email as the primary
    identifier and either find or create a local user record, then issue a JWT.
    """
    # Try to find existing user by email
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        # Create a new user with a random password (not intended for login)
        random_password = secrets.token_urlsafe(32)
        user = User(
            email=request.email,
            hashed_password=hash_password(random_password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Issue access token for this user
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
    )
