from pymongo import ASCENDING

from src.cross.mongo_client import get_mongo_collection

def list_perfumes_ordered_by_name(limit = 20, offset = 0):
    collection = get_mongo_collection("perfumes")
    perfumes_cursor = (collection
        .find(
            {},
            {
                "_id": 1,
                "name": 1,
                "brand": 1,
                "url": 1,
                "image_url": 1,
                "rating": 1
            }
        )
        .sort("name", ASCENDING)
        .skip(offset)
        .limit(limit))

    return list(perfumes_cursor)
