from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_user_id_from_request(request: Request):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError as e:
        print("⚠️ JWT decode failed:", e)
        return None

import uuid
from chromadb import Client

client = Client()

def add_memory(prompt: str, response: str, model: str, user_id: str):
    doc_id = str(uuid.uuid4())
    collection = client.get_or_create_collection(name="nava_memory")

    document = {
        "documents": [response],
        "metadatas": [{
            "prompt": prompt,
            "response": response,
            "model": model,
            "user_id": user_id
        }]
    }

    collection.add(
        ids=[doc_id],
        documents=document["documents"],
        metadatas=document["metadatas"]
    )
    return doc_id

# Example usage inside a function where `request`, `prompt`, `response`, `model` are available
# try:
#     user_id = get_user_id_from_request(request)
#     if user_id:
#         add_memory(
#             prompt=flat_text,
#             response=data["choices"][0]["message"]["content"],
#             model=model,
#             user_id=user_id
#         )
#     else:
#         print("⚠️ User ID not found — skipping memory save.")
# except Exception as mem_err:
#     print("⚠️ Memory storage failed:", mem_err)