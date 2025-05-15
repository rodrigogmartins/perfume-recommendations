from src.cross.mongo_client import get_mongo_collection

def search_perfumes_by_text(query, limit = 10, offset = 0):
    collection = get_mongo_collection("perfumes")
    return list(
        collection.find(
            { "$text": { "$search": query } },
            {
                "_id": 1,
                "name": 1,
                "brand": 1,
                "url": 1,
                "image_url": 1,
                "rating": 1
            }
        )
        .sort([
            ("score", {"$meta": "textScore"}),
            ("_id", 1)
        ])
        .skip(offset)
        .limit(limit)
    )
