from src.perfumes.utils.query_builder import query_builder


def test_excludes_owned_and_not_liked_perfumes():
    user_input = {
        "ownedPerfumes": ["id1"],
        "notLikedPerfumes": ["id2"],
        "notLikedNotes": [],
        "notLikedAccords": [],
        "likedNotes": [],
        "likedAccords": []
    }

    query = query_builder(user_input)

    assert query["_id"]["$nin"] == ["id1", "id2"]

def test_excludes_not_liked_notes_and_accords():
    user_input = {
        "ownedPerfumes": [],
        "notLikedPerfumes": [],
        "notLikedNotes": ["oud", "pine"],
        "notLikedAccords": ["balsamic"],
        "likedNotes": [],
        "likedAccords": []
    }

    query = query_builder(user_input)

    assert query["all_notes"] == {"$not": {"$elemMatch": {"$in": ["oud", "pine"]}}}
    assert query["accords"] == {"$not": {"$elemMatch": {"$in": ["balsamic"]}}}

def test_filters_by_day_shift_climate_season():
    user_input = {
        "ownedPerfumes": [],
        "notLikedPerfumes": [],
        "notLikedNotes": [],
        "notLikedAccords": [],
        "dayShifts": ["day"],
        "climates": ["cold"],
        "seasons": ["winter"],
        "likedNotes": [],
        "likedAccords": []
    }

    query = query_builder(user_input)

    assert query["day_shifts"] == {"$in": ["day"]}
    assert query["climates"] == {"$in": ["cold"]}
    assert query["seasons"] == {"$in": ["winter"]}

def test_includes_or_clauses_for_liked_notes_and_accords():
    user_input = {
        "ownedPerfumes": [],
        "notLikedPerfumes": [],
        "notLikedNotes": [],
        "notLikedAccords": [],
        "likedNotes": ["amber"],
        "likedAccords": ["woody"]
    }

    query = query_builder(user_input)

    assert "$or" in query
    assert {"all_notes": {"$in": ["amber"]}} in query["$or"]
    assert {"accords": {"$in": ["woody"]}} in query["$or"]

def test_does_not_add_or_clause_if_liked_lists_empty():
    user_input = {
        "ownedPerfumes": [],
        "notLikedPerfumes": [],
        "notLikedNotes": [],
        "notLikedAccords": [],
        "likedNotes": [],
        "likedAccords": []
    }

    query = query_builder(user_input)

    assert "$or" not in query
