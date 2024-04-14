from dotenv import load_dotenv
from fastapi import *
import uuid
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
import shutil

router = APIRouter()
load_dotenv()

# Setup MongoDB client
client = MongoClient(os.getenv('MONGO_URL', "mongodb://localhost:27017/"))
db = client['email_db']
users = db.users
webhook_uuid = os.getenv('WEBHOOK_UUID', 'default-uuid')

@router.post(f"/webhook/{webhook_uuid}")
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
