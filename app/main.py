from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import engine, Base
from app.routers import auth, listings, bookings
import app.models

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Airbnb Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "API চলছে ✅"}