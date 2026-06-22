from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.listing import Listing
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingUpdate, ListingResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/listings", tags=["Listings"])

# সব listing দেখা (সার্চ সহ)
@router.get("/", response_model=List[ListingResponse])
def get_listings(
    location   : str = None,
    min_price  : float = None,
    max_price  : float = None,
    max_guests : int = None,
    db         : Session = Depends(get_db)
):
    query = db.query(Listing)

    if location:
        query = query.filter(Listing.location.ilike(f"%{location}%"))
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    if max_guests:
        query = query.filter(Listing.max_guests >= max_guests)

    return query.all()

# একটি listing দেখা
@router.get("/{id}", response_model=ListingResponse)
def get_listing(id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

# নতুন listing তৈরি (শুধু host)
@router.post("/", response_model=ListingResponse)
def create_listing(
    data         : ListingCreate,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    if not current_user.is_host:
        raise HTTPException(status_code=403, detail="Only hosts can create listings")

    listing = Listing(**data.dict(), host_id=current_user.id)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

# listing আপডেট (শুধু নিজের)
@router.put("/{id}", response_model=ListingResponse)
def update_listing(
    id           : int,
    data         : ListingUpdate,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    listing = db.query(Listing).filter(Listing.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your listing")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(listing, key, value)

    db.commit()
    db.refresh(listing)
    return listing

# listing ডিলিট (শুধু নিজের)
@router.delete("/{id}")
def delete_listing(
    id           : int,
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    listing = db.query(Listing).filter(Listing.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your listing")

    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted ✅"}

# নিজের সব listing দেখা
@router.get("/my/listings", response_model=List[ListingResponse])
def my_listings(
    db           : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    return db.query(Listing).filter(Listing.host_id == current_user.id).all()