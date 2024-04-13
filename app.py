from fastapi import *
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import os
import shutil
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta
from User import User
import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

app = FastAPI()

# Load environment variables from .env file
load_dotenv()
webhook_uuid = os.getenv('WEBHOOK_UUID', 'default-uuid')

# Setup MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client['email_db']
users = db.users
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, Hash.SECRET_KEY, algorithms=[Hash.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/list-collections")
async def list_collections(current_user: str = Depends(get_current_user)):
    collections = db.list_collection_names()
    return {"collections": collections}

class EmailQuery(BaseModel):
    collection_name: str = Field(..., description="The name of the MongoDB collection.")
    email_filter: Optional[str] = Field(None, description="Filter emails by sender email")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of emails to return")

@app.post("/emails/")
async def list_emails(query: EmailQuery, current_user: str = Depends(get_current_user)):
    collection_name = query.collection_name
    if collection_name not in db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")

    collection = db[collection_name]

    filter_query = {}

    if query.email_filter:
        filter_query['to'] = query.email_filter

    emails = list(collection.find(filter_query).sort("received_at", -1).limit(query.limit))

    # Convert MongoDB documents to a more friendly format
    for email in emails:
        email['_id'] = str(email['_id'])

    return {"emails": emails}




@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    user_dict = user.dict()
    user_dict['password'] = Hash.hash_password(user_dict['password'])  # Implement password hashing
    user_dict['created_at'] = datetime.now()  # Set the creation time
    users.insert_one(user_dict)
    return {"message": "User created successfully"}

@app.get("/users/{username}")
async def read_user(username: str):
    user_data = users.find_one({"username": username}, {"_id": 0, "password": 0})
    if user_data:
        return user_data
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{username}")
async def update_user(username: str, user: User):
    updated_data = user.dict(exclude_unset=True)
    updated_data["updated_at"] = datetime.now()
    if "password" in updated_data:
        updated_data['password'] = Hash.hash_password(updated_data['password'])
    result = users.update_one({"username": username}, {"$set": updated_data})
    if result.modified_count:
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{username}")
async def delete_user(username: str):
    result = users.delete_one({"username": username})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/login")
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

@app.post(f"/webhook/{webhook_uuid}")
async def handle_webhook(
    request: Request,
    headers: str = Form(default=""),
    dkim: str = Form(default=""),
    html: str = Form(default=""),
    text: str = Form(default=""),
    from_email: str = Form(default="", alias="from"),
    to: str = Form(default=""),
    sender_ip: str = Form(default=""),
    spam_report: str = Form(default=""),
    envelope: str = Form(default=""),
    attachments_count: int = Form(default=""),
    subject: str = Form(default=""),
    spam_score: float = Form(default=""),
    charsets: str = Form(default=""),
    SPF: str = Form(default=""),
    files: list[UploadFile] = File(default=None)
):
    email_uuid = str(uuid.uuid4())
    recipient = to.split('@')[-1]
    collection = db[recipient] if recipient else db['default_collection']
    received_at = datetime.now()  # Captures the current date and time

    # Directory for attachments
    attachment_dir = f'/relay/attachments/{email_uuid}/'
    os.makedirs(attachment_dir, exist_ok=True)

    # Process attachments
    attachments = []

    if files:
        for file in files:
            if file.filename:
                file_uuid = str(uuid.uuid4())
                file_path = os.path.join(attachment_dir, f"{file_uuid}")
                
                with open(file_path, "wb+") as file_object:
                    shutil.copyfileobj(file.file, file_object)

                attachments.append({
                    'file_name': file.filename,
                    'file_uuid': file_uuid,
                    'file_path': file_path,
                    'content_type': file.content_type
                })

    # Construct document to insert into MongoDB
    email_data = {
        'email_uuid': email_uuid,
        'headers': headers,
        'dkim': dkim,
        'html': html,
        'text': text,
        'to': to,
        'from': from_email,
        'sender_ip': sender_ip,
        'spam_report': spam_report,
        'envelope': envelope,
        'attachments_count': len(attachments),
        'subject': subject,
        'spam_score': spam_score,
        'charsets': charsets,
        'SPF': SPF,
        'attachments': attachments,
        'received_at': received_at 
    }

    print(email_data)

    # Insert the email document into MongoDB
    collection.insert_one(email_data)
    
    return {"message": f"Email processed {email_uuid}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True, log_level='debug', access_log=True)
