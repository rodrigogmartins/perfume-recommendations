def query_builder(user_input_query):
    query = {
        "_id": {
            "$nin": user_input_query.get("ownedPerfumes", []) + user_input_query.get("notLikedPerfumes", [])
        },
        "all_notes": {
            "$not": {"$elemMatch": {"$in": user_input_query.get("notLikedNotes", [])}}
        },
        "accords": {
            "$not": {"$elemMatch": {"$in": user_input_query.get("notLikedAccords", [])}}
        }
    }
    if user_input_query.get("dayShifts"):
        query["day_shifts"] = {"$in": user_input_query["dayShifts"]}
    if user_input_query.get("climates"):
        query["climates"] = {"$in": user_input_query["climates"]}
    if user_input_query.get("seasons"):
        query["seasons"] = {"$in": user_input_query["seasons"]}

    liked_clauses = []
    if user_input_query.get('likedNotes'):
        liked_clauses.append({"all_notes": {"$in": user_input_query['likedNotes']}})
    if user_input_query.get('likedAccords'):
        liked_clauses.append({"accords": {"$in": user_input_query['likedAccords']}})
    if liked_clauses:
        query["$or"] = liked_clauses

    return query
