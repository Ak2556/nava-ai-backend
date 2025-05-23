from fastapi import HTTPException, Request
from jose import jwt, JWTError
import os
import httpx
import traceback

from app.core.config import get_openrouter_key
from app.services.chroma_service import add_memory

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_user_id_from_request(request: Request):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

async def call_openrouter(messages: list, request: Request) -> dict:
    """
    Calls OpenRouter with full message history and retries manually.
    Returns the assistant reply and model name used.
    """
    try:
        print("📨 call_openrouter() received messages:")

        for i, m in enumerate(messages):
            try:
                print(f"{i + 1}. {m['role'].upper()}: {m['content']}")
            except Exception as err:
                print(f"⚠️ Invalid message format at index {i}: {m} — {err}")

        # Combine all user messages to estimate token usage
        flat_text = " ".join([
            m["content"] for m in messages if m.get("role") == "user"
        ])

        if len(flat_text.split()) > 1500:
            raise HTTPException(status_code=400, detail="Prompt too long. Please shorten it.")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {get_openrouter_key()}",
            "Content-Type": "application/json"
        }

        fallback_models = [
            "openai/gpt-4o-mini",
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3.5-sonnet"
        ]

        for model in fallback_models:
            for attempt in range(3):
                try:
                    print(f"🧠 Attempt {attempt+1} using model: {model}")

                    body = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": 512,
                        "temperature": 0.7
                    }

                    async with httpx.AsyncClient(timeout=10) as client:
                        response = await client.post(url, headers=headers, json=body)
                        data = response.json()

                    print(f"📥 {model} responded with:", data)

                    if response.status_code == 200 and "choices" in data:
                        try:
                            user_id = get_user_id_from_request(request)
                            if user_id:
                                add_memory(
                                    prompt=flat_text,
                                    response=data["choices"][0]["message"]["content"],
                                    model=model,
                                    user_id=user_id
                                )
                        except Exception as mem_err:
                            print("⚠️ Memory storage failed:", mem_err)

                        return {
                            "model": model,
                            "content": data["choices"][0]["message"]["content"]
                        }

                    if "error" in data and data["error"].get("code") == 402:
                        print("💸 Credit issue. Skipping to next model.")
                        break  # Try next model

                except Exception as err:
                    print(f"❌ Error on attempt {attempt+1} with model {model}:")
                    traceback.print_exception(type(err), err, err.__traceback__)

        raise HTTPException(status_code=502, detail="All models failed after retries.")

    except Exception as e:
        print("🔥 Unhandled fatal error in call_openrouter():")
        traceback.print_exception(type(e), e, e.__traceback__)
        raise HTTPException(status_code=500, detail="Something went wrong. Check logs.")