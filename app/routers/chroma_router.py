

from fastapi import APIRouter, HTTPException
from chromadb import Client
from pydantic import BaseModel
from app.services.chroma_service import add_memory, query_memory, wipe_memory

router = APIRouter(prefix="/chroma", tags=["ChromaDB"])

class MemoryInput(BaseModel):
    id: str
    content: str
    metadata: dict = {}

class QueryInput(BaseModel):
    query: str
    top_k: int = 3

@router.post("/add")
def add_to_memory(payload: MemoryInput):
    try:
        add_memory(payload.id, payload.content, payload.metadata)
        return {"status": "success", "message": "Memory added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
def query_memory_route(query_input: QueryInput):
    try:
        results = query_memory(query_input.query, query_input.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wipe")
def wipe_memory_route():
    try:
        wipe_memory()
        return {"status": "success", "message": "Memory wiped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def get_user_memory(user_id: str):
    try:
        client = Client()
        collection = client.get_or_create_collection(name="nava_memory")
        results = collection.get(where={"user_id": user_id})
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))