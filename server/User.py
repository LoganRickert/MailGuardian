from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from datetime import datetime 

class Permission(BaseModel):
    collection_name: str
    emails: List[EmailStr]
    can_read: bool = False
    can_send: bool = False

class User(BaseModel):
    username: str
    password: str  # In production, ensure this is hashed before storing
    role: str = Field(..., pattern="^(viewer|member|admin)$")
    permissions: List[Permission]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "s3cr3t",  # Reminder: Hash this password in real scenarios
                "role": "member",
                "permissions": [
                    {
                        "domain": "example.com",
                        "emails": ["user@example.com"],
                        "can_read": True,
                        "can_send": False
                    }
                ]
            }
        }
