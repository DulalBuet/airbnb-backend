from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.booking import Booking
from app.models.listing import Listing
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# নতুন বুকিং তৈরি
@router.post("/", response_model=BookingResponse)
def create_booking(
    data         : BookingCreate,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    # listing আছে কিনা চেক
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # নিজের listing বুক করা যাবে না
    if listing.host_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot book your own listing")

    # তারিখ ঠিক আছে কিনা চেক
    if data.check_in >= data.check_out:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    # তারিখ কনফ্লিক্ট চেক
    conflict = db.query(Booking).filter(
        Booking.listing_id == data.listing_id,
        Booking.status != "cancelled",
        Booking.check_in  < data.check_out,
        Booking.check_out > data.check_in
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Listing not available for these dates")

    # মোট দাম হিসাব
    days = (data.check_out - data.check_in).days
    total_price = days * listing.price

    booking = Booking(
        listing_id  = data.listing_id,
        guest_id    = current_user.id,
        check_in    = data.check_in,
        check_out   = data.check_out,
        total_price = total_price,
        status      = "confirmed"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

# আমার সব বুকিং দেখা (guest হিসেবে)
@router.get("/my", response_model=List[BookingResponse])
def my_bookings(
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    return db.query(Booking).filter(Booking.guest_id == current_user.id).all()

# একটি বুকিং দেখা
@router.get("/{id}", response_model=BookingResponse)
def get_booking(
    id           : int,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.guest_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    return booking

# বুকিং ক্যান্সেল করা
@router.patch("/{id}/cancel", response_model=BookingResponse)
def cancel_booking(
    id           : int,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.guest_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Already cancelled")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking

# হোস্ট হিসেবে নিজের listing এর সব বুকিং দেখা
@router.get("/host/all", response_model=List[BookingResponse])
def host_bookings(
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    listings = db.query(Listing).filter(Listing.host_id == current_user.id).all()
    listing_ids = [l.id for l in listings]
    return db.query(Booking).filter(Booking.listing_id.in_(listing_ids)).all()