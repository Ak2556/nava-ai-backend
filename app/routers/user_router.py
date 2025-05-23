from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import UserResponse, ModelUpdateRequest
from app.auth import get_current_user

router = APIRouter()

VALID_MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-3.5-turbo",
    "anthropic/claude-3.5-sonnet",
    "mistral/mixtral-8x7b"
]

@router.post("/user/model", response_model=UserResponse)
def update_model_preference(
    payload: ModelUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"📥 Incoming model update request: {payload.model}")
    print(f"🔐 Current user: {current_user.email} (ID: {current_user.id})")

    if payload.model not in VALID_MODELS:
        print("❌ Invalid model selected.")
        raise HTTPException(status_code=400, detail="Invalid model selected.")

    try:
        current_user.model_preference = payload.model
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        print("✅ Model updated successfully.")
        return current_user

    except Exception as e:
        db.rollback()
        print(f"🔥 Failed to update model preference: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")