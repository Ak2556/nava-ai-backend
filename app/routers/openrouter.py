from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.openrouter_service import call_openrouter
# 🛠 Remove faulty imports for now — we'll add them once they're fixed

router = APIRouter()

# ✅ Pydantic schema for chat messages
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@router.post("/openrouter")
async def openrouter_route(request: Request, body: ChatRequest):
    """
    Sends message history to OpenRouter and returns assistant's response.
    """
    try:
        print("🧠 Incoming /openrouter request:")
        for msg in body.messages:
            print(f"{msg.role.upper()}: {msg.content}")

        raw_messages = [msg.dict() for msg in body.messages]
        response = await call_openrouter(raw_messages, request)
        return response

    except Exception as e:
        print("❌ Error in /openrouter route:", e)
        raise HTTPException(status_code=500, detail="Internal server error in OpenRouter route.")