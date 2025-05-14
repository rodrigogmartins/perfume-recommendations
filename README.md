# Perfume recommendation based on user preferences

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md) [![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](./docs/README.pt-br.md)

## Use Case
This application aims to provide intelligent perfume recommendations based on each user's personal preferences. The API allows users to specify which perfumes they own, which ones they like or dislike, as well as olfactory notes and accords they enjoy or wish to avoid.

Based on this information, combined with contextual data — such as weather, season, and time of day the perfume will be worn — the API filters and suggests ideal perfumes, respecting preference criteria and avoiding unwanted or already owned fragrances.

The stored perfume database contains rich attributes such as accords, notes, usage recommendations, and illustrative images. Recommendations are generated dynamically: users can provide custom filters in the API request or, if they prefer, the recommendation will be based solely on their saved profile in the database.

This approach makes the experience highly personalized, useful both for consumers looking for their next ideal fragrance and for e-commerce platforms or marketplaces that want to offer more accurate and contextual recommendations.


## 🚀 Step-by-Step Guide to the Perfume Recommendation Process

### 1. 📥 Receiving the Request

The API receives a request with the following payload (all fields are optional):

```json
{
   "ownedPerfumes": ["1", "2", "3"],
   "likedPerfumes": ["3"],
   "notLikedPerfumes": ["4"],
   "likedNotes": ["vanilla", "eucalyptus"],
   "notLikedNotes": ["pine", "oud"],
   "likedAccords": ["leather", "sweet"],
   "notLikedAccords": ["balsamic", "powdery"], 
   "dayShifts": ["night"], 
   "climates": ["cold"],
   "seasons": ["winter", "spring"]
}
```


### 2. 🧠 Defining the Filtering Criteria

- If the request input contains filters, they are used.
- Otherwise, the data previously saved in the user's profile is used.
- If no data is available, the system may return generic or popular perfumes (optional).

### 3. 🧩 Data Enrichment with Inference

For perfumes that lack usage information (weather, time of day, season), the system infers this data based on accords using predefined rules.

### 4. 🔍 Building the MongoDB Query

The query applies the following rules:

- ❌ Excludes:
  - Perfumes the user already owns.
  - Perfumes the user dislikes.
  - Perfumes with notes or accords the user dislikes.

- ✅ Includes:
  - Perfumes compatible with the specified weather, time of day, and season.
  - Perfumes with preferred notes/accords.
  - Perfumes similar to those the user likes, based on the most common notes and accords among them.


### 5. 🎯 Result Prioritization

Perfumes are ranked based on:
- Compatibility with the usage context (e.g., exclusively nighttime if "night" was requested).
- Number of shared characteristics with perfumes the user likes.
- Presence of desired notes and accords.


### 6. 📤 Returning the Recommendation
- The API returns up to 10 recommended perfumes.
- Example response:

```json
{
  "items": [
    {
      "_id": "23569",
      "name": "shisha-lounge",
      "brand": "ricardo-ramos-perfumes-de-autor",
      "top_notes": [ "anise", "red fruits", "hazelnut", "neroli" ],
      "mid_notes": [ "tobacco", "labdanum", "oakmoss", "patchouli" ],
      "base_notes": [ "amber", "madagascar vanilla", "tonka bean", "musk" ],
      "accords": [ "sweet", "amber", "anis", "soft spicy", "tobacco" ],
      "day_shifts": [ "night" ],
      "climates": [ "cold" ],
      "seasons": [ "winter" ],
      "url": "https://www.fragrantica.com/perfume/ricardo-ramos-perfumes-de-autor/shisha-lounge-58575.html",
      "image_url": "https://fimgs.net/mdimg/perfume/375x500.58575.jpg",
      "rating": 4.46,
      "match_probability": 0.53
    }
  ]
}
```

---

## 📡 API Endpoints

### 🔎 GET ```/api/perfumes/search```

If a ```query``` is passed, then performs a perfume search using full-text search.
Else, returns a list of perfumes in alphabetical order.

#### Parâmetros de query:
- ```query``` **(optional)**  — search term.
- ```limit``` **(optional, default: 10)**.
- ```offset``` (optional, default: ```0```) — number of items to skip before starting to collect results (for pagination).

#### Example Request:
```bash
  curl --request GET \
    --url 'http://localhost:8000/api/perfumes/search?query=invictus&limit=20&offset=0'
```

#### Example Response:
```json
{
  "items": [
    {
      "id": "646",
      "name": "Acqua di Gio",
      "brand": "Giorgio Armani",
      "url": "https://www.fragrantica.com/perfume/Giorgio-Armani/Acqua-di-Gio-646.html",
      "image_url": "https://fimgs.net/mdimg/perfume/375x500.646.jpg",
      "rating": 3.73
    }
  ]
}
```

### 🎯 POST ```/api/perfumes/recommendations```

Generates a personalized list of perfumes based on the user's preferences and/or previously stored data.

#### Parâmetros de query:
- ```limit``` **(optional, max: 10)**.

#### Body (JSON):
All fields are optional.

```json
{
  "ownedPerfumes": ["1", "2", "3"],
  "likedPerfumes": ["3", "4"],
  "notLikedPerfumes": [],
  "notLikedNotes": ["pine", "oud"],
  "notLikedAccords": ["balsamic", "powdery"],
  "dayShifts": ["night"],
  "climates": ["cold"]
}
```

#### Example Request:
```bash
  curl --request POST \
    --url http://localhost:8000/api/perfumes/recommendations?limit=1 \
    --header 'Content-Type: application/json' \
    --scripts '{
      "ownedPerfumes": ["1", "2", "3"],
      "likedPerfumes": ["1", "4"],
      "notLikedPerfumes": [],
      "notLikedNotes": ["pine", "oud"],
      "notLikedAccords": ["balsamic", "powdery"],
      "dayShifts": ["night"],
      "climates": ["cold"]
    }'
```

#### Example Response:
```json
{
  "items": [
    {
      "name": "Hero Boadicea the Victorious",
      "brand": "Boadicea The Victorious",
      "top_notes": [ "hazelnut", "saffron", "coffee", "rhubarb", "ylang-ylang" ],
      "mid_notes": [ "tobacco", "patchouli", "tonka bean", "sandalwood", "rose" ],
      "base_notes": [ "guaiac wood", "indian oud", "fir resin", "siam benzoin", "cypriol oil or nagarmotha", "rock rose" ],
      "accords": [ "woody", "warm spicy", "sweet", "tobacco", "nutty" ],
      "day_shifts": [ "night" ],
      "climates": [ "cold" ],
      "seasons": [ "winter", "fall" ],
      "url": "https://www.fragrantica.com/perfume/boadicea-the-victorious/hero-37792.html",
      "image_url": "https://fimgs.net/mdimg/perfume/375x500.37792.jpg",
      "rating": 4.49,
      "match_probability": 0.53,
      "id": "23569"
    }
  ]
}
```

#### Notes:
- The ```score``` field represents the estimated probability that the user will like the perfume.
- Perfumes the user already owns, dislikes, or that contain disliked notes/accords are automatically excluded.

---

## 🛠️ Step-by-Step Guide to Run the Project Locally

### 1. 📦 Prerequisites

Make sure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10+ com `pip`


### 2. 🐳 Bringing Up Services with Docker Compose

1. Clone the project repository:

```bash
  git clone https://github.com/rodrigogmartins/perfume-recommendations.git
  cd perfume-recommendations
```

2. Start MongoDB:

```bash
  docker-compose up -d
```


### 3. 📚 Create a Virtual Environment and Install Dependencies

```bash
  python -m venv venv
  source venv/bin/activate  # no Windows use: venv\Scripts\activate
  pip install -r requirements.txt
```


### 4. 📥 Populate the Database with Perfumes

Run the script to save perfume data from the dataset into MongoDB:

```bash
  python -m scripts.fill_perfume_dataset
```

This script:
- Reads the .csv file with perfumes
- Makes usage inference (weather, season, time of day)
- Builds the perfume image URL.
- Inserts perfumes into the perfumes collection in MongoDB

#### 4.1. Query perfumes from Database

```bash
  docker exec -it mongodb mongosh -u root -p example
  use perfume_db
  db.perfumes.find().limit(5).pretty()
```

### 5. 🚀 Run the API

With everything installed, run the application locally:

```bash
  python server.py
```

The API will be available at: http://localhost:8000


### 6. 📘 Access the Documentation

Access the Swagger API documentation:

```bash
  http://localhost:8000/docs
```

### 7. 🧹 Stop the Services

To stop the Docker services:

```bash
  docker-compose down
```

---

## 📊 Data Used

This project uses data collected from the Fragrantica user community, organized in the "Fragrantica.com Fragrance Dataset" available at [https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset).

**Credits:**  
Dataset organized by [Olga G](https://www.kaggle.com/olgagmiufana1)  
License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Modifications were made for inferring weather, season, and time of day for perfume usage.  
Distribution and usage are in compliance with the license, for non-commercial purposes.


