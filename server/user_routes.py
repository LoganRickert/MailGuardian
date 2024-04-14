from User import User
from fastapi import *
import Hash
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import uuid

router = APIRouter()
load_dotenv()

# Setup MongoDB client
client = MongoClient(os.getenv('MONGO_URL', "mongodb://localhost:27017/"))
db = client['email_db']
users = db.users

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    user_dict = user.dict()
    user_dict['uuid'] = str(uuid.uuid4())
    user_dict['password'] = Hash.hash_password(user_dict['password'])  # Implement password hashing
    user_dict['created_at'] = datetime.now()  # Set the creation time
    users.insert_one(user_dict)
    return {"message": "User created successfully"}

@router.get("/users/{username}")
async def read_user(username: str):
    user_data = users.find_one({"username": username}, {"_id": 0, "password": 0})
    if user_data:
        return user_data
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{username}")
async def update_user(username: str, user: User):
    updated_data = user.dict(exclude_unset=True)
    updated_data["updated_at"] = datetime.now()
    if "password" in updated_data:
        updated_data['password'] = Hash.hash_password(updated_data['password'])
    result = users.update_one({"username": username}, {"$set": updated_data})
    if result.modified_count:
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{username}")
async def delete_user(username: str):
    result = users.delete_one({"username": username})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"username": form_data.username})
    if not user or not Hash.verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Hash.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Hash.create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
