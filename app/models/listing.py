from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id          = Column(Integer, primary_key=True, index=True)
    host_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    title       = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price       = Column(Float, nullable=False)
    location    = Column(String, nullable=False)
    image_url   = Column(String, nullable=True)
    max_guests  = Column(Integer, default=1)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    host        = relationship("User", back_populates="listings")
    bookings    = relationship("Booking", back_populates="listing")