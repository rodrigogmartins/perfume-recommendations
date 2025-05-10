from pymongo import DESCENDING

from src.cross.mongo_client import get_mongo_collection
from src.perfumes.calculate_affinity_score import calculate_affinity_score
from src.perfumes.prioritizer.perfumes_prioritizer import perfumes_prioritizer
from src.perfumes.utils.query_builder import query_builder


def get_sorted_perfumes(user_input_query):
    collection = get_mongo_collection("perfumes")
    query = query_builder(user_input_query)
    perfumes = (
        collection.find(
            query,
            {
                "_id": 1,
                "name": 1,
                "brand": 1,
                "top_notes": 1,
                "mid_notes": 1,
                "base_notes": 1,
                "accords": 1,
                "day_shifts": 1,
                "climates": 1,
                "seasons": 1,
                "url": 1,
                "image_url": 1,
                "rating": 1,
            }
        )
        .sort("rating", DESCENDING)
    )
    recommended_perfumes = sorted(
        perfumes,
        key=lambda perfume: perfumes_prioritizer(perfume, user_input_query),
        reverse=True
    )[:10]

    for recommended_perfume in recommended_perfumes:
        recommended_perfume["match_probability"] = calculate_affinity_score(recommended_perfume, user_input_query)

    return recommended_perfumes
