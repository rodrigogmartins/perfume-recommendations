def format_perfumes_ids(perfumes):
    return [format_perfume_id(doc) for doc in perfumes]

def format_perfume_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc