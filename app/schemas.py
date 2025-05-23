from pydantic import BaseModel, EmailStr
from typing import Optional

# 🔐 For user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 🔐 For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 🔄 For updating model preference
class ModelUpdateRequest(BaseModel):
    model: str

# 📤 For responses (exposed to frontend)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_preference: Optional[str] = "openai/gpt-4o-mini"

    class Config:
        orm_mode = True  # older naming, compatible with older Pydantic
        # or for Pydantic v2:
        # from_attributes = True

# 💬 For incoming chat messages
class MessageSchema(BaseModel):
    role: str
    content: str

    class Config:
        orm_mode = True  # same note applies here