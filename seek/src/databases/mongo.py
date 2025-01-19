import os

from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "seek_db")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?ssl=false"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
