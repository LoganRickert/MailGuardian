from pymongo import MongoClient
from fastapi import *
import Hash
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

# Setup MongoDB client
client = MongoClient(os.getenv('MONGO_URL', "mongodb://localhost:27017/"))
db = client['email_db']
users = db.users

@router.get("/domains")
async def list_domains(current_user: str = Depends(Hash.get_current_user)):
    collections = db.list_collection_names()
    
    # Filter collections to include only those with periods in their names
    filtered_collections = [name for name in collections if '.' in name]
    
    return {"domains": filtered_collections}
