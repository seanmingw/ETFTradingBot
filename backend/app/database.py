"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    positions = relationship("UserPosition", back_populates="user")
    trades = relationship("Trade", back_populates="user")

class UserPosition(Base):
    """User position model."""
    __tablename__ = "user_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False, index=True)
    fund_type = Column(String(20), nullable=False)  # 'exchange' (场内) or 'offline' (场外)
    name = Column(String(200))
    quantity = Column(Integer, default=0)
    avg_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="positions")

class Trade(Base):
    """Trade history model."""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False, index=True)
    fund_type = Column(String(20), nullable=False)
    action = Column(String(10), nullable=False)  # 'buy' or 'sell'
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    commission = Column(Float, default=1.0)
    total_amount = Column(Float, nullable=False)
    strategy = Column(String(50), default="manual")
    status = Column(String(20), default="FILLED")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="trades")
