import pandas as pd
import uuid
from pymongo import MongoClient, ASCENDING

from src.data.inferences.perfume_climates_usage_recommendations_inference import get_climates_recommendations_inference
from src.data.inferences.perfume_seasons_usage_recommendations_inference import get_seasons_recommendations_inference
from src.data.inferences.perfume_day_shifts_usage_recommendations_inference import \
    get_day_shifts_recommendations_inference

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["perfume_db"]
collection = db["perfumes"]
collection.drop()

collection.create_index([("name", ASCENDING)])
collection.create_index([("brand", ASCENDING)])
collection.create_index([("accords", ASCENDING)])
collection.create_index([("day_shifts", ASCENDING)])
collection.create_index([("climates", ASCENDING)])
collection.create_index([("seasons", ASCENDING)])

df = pd.read_csv("datasets/fra_cleaned.csv", sep=";", encoding="latin1")

perfumes = []

def get_accords(row_param):
    accords_list = [row_param[f"mainaccord{i}"] for i in range(1, 6) if pd.notna(row_param[f"mainaccord{i}"])]
    return [a.lower().strip() for a in accords_list]

for _, row in df.iterrows():
    try:
        accords = get_accords(row)
        perfume = {
            "_id": str(uuid.uuid4()),
            "name": row["Perfume"].strip(),
            "brand": row["Brand"].strip(),
            "country": row["Country"].strip(),
            "gender": row["Gender"].strip(),
            "year": row["Year"],
            "top_notes": row['Top'].split(", "),
            "mid_notes": row['Middle'].split(", "),
            "base_notes": row['Base'].split(", "),
            "all_notes": row['Top'].split(", ") + row['Middle'].split(", ") + row['Base'].split(", "),
            "accords": accords,
            "day_shifts": get_day_shifts_recommendations_inference(accords),
            "climates": get_climates_recommendations_inference(accords),
            "seasons": get_seasons_recommendations_inference(accords),
            "url": row["url"].strip()
        }
        perfumes.append(perfume)
    except Exception as e:
        print(f"Error trying to process line: {e}, {row}")


if perfumes:
    collection.insert_many(perfumes)
    print(f"{len(perfumes)} perfume saved with success!")
else:
    print("No processed perfume")