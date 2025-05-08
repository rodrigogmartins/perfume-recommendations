from pymongo import MongoClient

_client = None
_db = None

def get_mongo_collection(collection_name):
    global _client, _db

    if _client is None:
        _client = MongoClient("mongodb://root:example@localhost:27017/")

    if _db is None:
        _db = _client["perfume_db"]

    return _db[collection_name]
