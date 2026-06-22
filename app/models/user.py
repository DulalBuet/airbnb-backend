from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    is_host    = Column(Boolean, default=False)
    avatar     = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    listings   = relationship("Listing", back_populates="host")
    bookings   = relationship("Booking", back_populates="guest")