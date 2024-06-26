from fastapi import *
from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel, Field
import Hash
import os

router = APIRouter()

# Setup MongoDB client
client = MongoClient(os.getenv('MONGO_URL', "mongodb://localhost:27017/"))
db = client['email_db']
users = db.users

class EmailQuery(BaseModel):
    email_filter: str = Field(None, description="Filter emails by sender email")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of emails to return")

@router.post("/emails/")
async def list_emails(query: EmailQuery, current_user: str = Depends(Hash.get_current_user)):
    first_email = query.email_filter

    if not first_email:
        raise HTTPException(status_code=404, detail="No emails listed")

    domain = first_email.split("@")[-1]

    print("Checking Domain", domain, first_email)

    if domain not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Domain not found")

    collection = db[domain]

    filter_query = {}

    if query.email_filter:
        filter_query['to'] = query.email_filter

    emails = list(collection.find(filter_query).sort("received_at", -1).limit(query.limit))

    # Convert MongoDB documents to a more friendly format
    for email in emails:
        email['_id'] = str(email['_id'])

    return {"emails": emails}
