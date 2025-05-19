import os

from urllib.parse import quote_plus
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING

from scripts.inferences.perfume_climates_usage_recommendations_inference import get_climates_recommendations_inference
from scripts.inferences.perfume_day_shifts_usage_recommendations_inference import \
    get_day_shifts_recommendations_inference
from scripts.inferences.perfume_seasons_usage_recommendations_inference import get_seasons_recommendations_inference


load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_DB = os.getenv("MONGO_DB")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

collection = db["perfumes"]
collection.drop()

collection.create_index([("name", ASCENDING)])
collection.create_index([("brand", ASCENDING)])
collection.create_index([("accords", ASCENDING)])
collection.create_index([("day_shifts", ASCENDING)])
collection.create_index([("climates", ASCENDING)])
collection.create_index([("seasons", ASCENDING)])
collection.create_index([("rating", DESCENDING)])
collection.create_index([
    ("name", "text"),
    ("brand", "text"),
    ("description", "text")
])

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

perfumes_data_cleaned = pd.read_csv(os.path.join(SCRIPT_DIR, 'datasets', 'fra_cleaned.csv'), sep=";", encoding="latin1")
perfumes_data = pd.read_csv(os.path.join(SCRIPT_DIR, 'datasets', 'fra_perfumes.csv'), sep=",", encoding="utf-8").to_dict(orient="records")

perfumes = []
url_index = {
    item["url"].strip().lower(): item
    for item in perfumes_data
    if "url" in item and item["url"]
}

def get_accords(row_param):
    accords_list = [row_param[f"mainaccord{i}"] for i in range(1, 6) if pd.notna(row_param[f"mainaccord{i}"])]
    return [a.lower().strip() for a in accords_list]

def format_perfume_name(slug):
    return ' '.join(word.capitalize() for word in slug.split('-'))

def generate_image_url(product_url):
    try:
        perfume_id = product_url.rstrip('/').split('-')[-1].replace('.html', '')
        return f"https://fimgs.net/mdimg/perfume/375x500.{perfume_id}.jpg"
    except Exception as e:
        raise ValueError(f"Erro ao gerar imagem a partir da URL '{product_url}': {e}")

for index, row in perfumes_data_cleaned.iterrows():
    try:
        item = url_index.get(row["url"].strip().lower())

        if (item is None) or (item == ""):
            continue

        accords = get_accords(row)
        perfume = {
            "_id": str(index),
            "name": item["Name"].replace(item["Gender"], ""),
            "brand": format_perfume_name(row["Brand"].strip()),
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
            "url": row["url"].strip(),
            "image_url": generate_image_url(row["url"].strip()),
            "rating": item["Rating Value"]
        }
        perfumes.append(perfume)
    except Exception as e:
        print(f"Error trying to process line: {e}, {row}")


if perfumes:
    collection.insert_many(perfumes)
    print(f"{len(perfumes)} perfume saved with success!")
else:
    print("No processed perfume")