from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import auth_router
from app.db import Base, engine
from app import models  # Required to register SQLAlchemy models
from app.routers import openrouter, user_router

app = FastAPI(
    title="Nava-AI Backend",
    description="FastAPI backend with OpenRouter + ChromaDB memory",
    version="1.0.0",
)

# ✅ CORS middleware — allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Auto-create tables on first run (comment out after initial use)
Base.metadata.create_all(bind=engine)

# ✅ Include all routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(openrouter.router)
app.include_router(user_router.router, prefix="/user", tags=["User"])