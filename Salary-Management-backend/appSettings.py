from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
FRONTEND_URL = os.environ.get("FRONTEND_URL")
BACKEND_CORS_ORIGINS = os.environ.get("BACKEND_CORS_ORIGINS", "").strip("[]").replace('"', '').split(',') if os.environ.get("BACKEND_CORS_ORIGINS") else FRONTEND_URL
SECURE_HTTPS_COOKIE = False

if SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS if BACKEND_CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Salary Management API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}