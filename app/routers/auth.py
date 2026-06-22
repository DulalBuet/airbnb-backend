from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import RegisterSchema, LoginSchema, UserResponse
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    # email আগে থেকে আছে কিনা চেক
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name     = data.name,
        email    = data.email,
        password = hash_password(data.password),
        is_host  = data.is_host
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})
    return {
        "access_token" : token,
        "token_type"   : "bearer",
        "user"         : {
            "id"     : user.id,
            "name"   : user.name,
            "email"  : user.email,
            "is_host": user.is_host
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user