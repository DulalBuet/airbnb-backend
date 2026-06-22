from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    listing_id : int
    check_in   : datetime
    check_out  : datetime

class BookingResponse(BaseModel):
    id          : int
    listing_id  : int
    guest_id    : int
    check_in    : datetime
    check_out   : datetime
    total_price : float
    status      : str
    created_at  : datetime

    class Config:
        from_attributes = True