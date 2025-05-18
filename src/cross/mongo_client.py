from urllib.parse import quote_plus
import os
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_DB = os.getenv("MONGO_DB")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?tls=true&tlsCAFile=/app/certs/rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"

_client = None
_db = None

def get_mongo_collection(collection_name):
    global _client, _db

    if _client is None:
        _client = MongoClient(MONGO_URI)

    if _db is None:
        _db = _client[MONGO_DB]

    return _db[collection_name]
