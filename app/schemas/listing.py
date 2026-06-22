from pydantic import BaseModel
from datetime import datetime

class ListingCreate(BaseModel):
    title       : str
    description : str
    price       : float
    location    : str
    max_guests  : int = 1
    image_url   : str | None = None

class ListingUpdate(BaseModel):
    title       : str | None = None
    description : str | None = None
    price       : float | None = None
    location    : str | None = None
    max_guests  : int | None = None
    image_url   : str | None = None

class ListingResponse(BaseModel):
    id          : int
    host_id     : int
    title       : str
    description : str
    price       : float
    location    : str
    max_guests  : int
    image_url   : str | None
    created_at  : datetime

    class Config:
        from_attributes = True