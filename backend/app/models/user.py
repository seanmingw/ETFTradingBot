"""User models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic import BaseModel as PydanticBaseModel

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserProfile(UserResponse):
    total_invested: float = 0.0
    total_profit: float = 0.0
    positions_count: int = 0
