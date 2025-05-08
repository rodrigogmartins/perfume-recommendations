from src.controller.user_input_query import UserInputQuery
from src.cross.mongo_client import get_mongo_collection
from src.perfumes.utils.get_effective_liked_accords import get_effective_liked_accords
from src.perfumes.utils.get_effective_liked_notes import get_effective_liked_notes

def user_input_query_builder(user_input: UserInputQuery):
    collection = get_mongo_collection("perfumes")

    liked_perfumes_query = { "_id": { "$in": user_input.likedPerfumes } }
    liked_perfumes_collection = collection.find(liked_perfumes_query, { "all_notes": 1, "accords": 1})
    liked_perfumes = list(liked_perfumes_collection)

    return {
        "ownedPerfumes": user_input.ownedPerfumes,
        "likedPerfumes": user_input.likedPerfumes,
        "notLikedPerfumes": user_input.notLikedPerfumes,
        "likedNotes": get_effective_liked_notes(liked_perfumes, user_input.likedNotes),
        "notLikedNotes": user_input.notLikedNotes,
        "likedAccords": get_effective_liked_accords(liked_perfumes, user_input.likedAccords),
        "notLikedAccords": user_input.notLikedAccords,
        "dayShifts": user_input.dayShifts,
        "climates": user_input.climates,
        "seasons": user_input.seasons
    }