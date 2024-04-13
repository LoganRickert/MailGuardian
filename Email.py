from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Any, Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, field: Field):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        return {
            "type": "string",
            "pattern": "^[a-fA-F0-9]{24}$",  # Regex for MongoDB ObjectIds
        }

class Email(BaseModel):
    id: PyObjectId = Field(alias='_id')
    from_email: Optional[str] = Field(None, alias='from')
    subject: str
    received_at: Optional[str] = None

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }
        populate_by_name = True  # Updated configuration key for Pydantic v2
