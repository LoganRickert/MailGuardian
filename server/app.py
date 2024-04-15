from fastapi import *
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

from user_routes import router as user_router
from email_routes import router as email_router
from webhook_routes import router as webhook_routes
from domain_routes import router as domain_routes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(email_router, prefix="/api/v1", tags=["emails"])
app.include_router(webhook_routes, prefix="/api/v1", tags=["webhooks"])
app.include_router(domain_routes, prefix="/api/v1", tags=["domains"])

# Load environment variables from .env file
load_dotenv()

# Setup MongoDB client
client = MongoClient(os.getenv('MONGO_URL', "mongodb://localhost:27017/"))
db = client['email_db']
users = db.users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True, log_level='debug', access_log=True)
