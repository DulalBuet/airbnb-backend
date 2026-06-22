from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id          = Column(Integer, primary_key=True, index=True)
    listing_id  = Column(Integer, ForeignKey("listings.id"), nullable=False)
    guest_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in    = Column(DateTime, nullable=False)
    check_out   = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    status      = Column(String, default="pending")  # pending, confirmed, cancelled
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    listing     = relationship("Listing", back_populates="bookings")
    guest       = relationship("User", back_populates="bookings")