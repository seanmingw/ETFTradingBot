"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..auth import (
    get_db, hash_password, verify_password, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, create_database
)
from ..database import User
from ..models.user import UserCreate, UserResponse, Token, UserLogin

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    create_database()

    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    create_database()

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login."""
    create_database()

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(db: Session = Depends(get_db)):
    """Get current user information."""
    from ..auth import get_current_user
    from fastapi import Depends
    from fastapi.security import OAuth2PasswordBearer

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

    async def get_user():
        from ..auth import decode_token
        from fastapi import HTTPException

        token = oauth2_scheme
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        token_data = decode_token(token)
        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    return await get_user()
